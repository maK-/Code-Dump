/*
compile with-
gcc -o assignment2 assignment2.c -pthread -lrt

One thread creates an alarm in the near future, 
second thread then alerts the time.

*/
#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <time.h>
#define ETIMEDOUT 110

//Wakeup call.
typedef struct {
	time_t time;
	int roomNo;
} WakeUp;

//Heap of calls.
typedef struct {
	int size;
	WakeUp *wakeups;
	pthread_mutex_t lock;
  	pthread_cond_t cond;
} WakeUpHeap;

//Finding the right place to insert an item into the heap.
void siftUp(WakeUpHeap* heap, int index) {
	int parentIndex;
	WakeUp tmp;
	if(index != 0) {
		parentIndex = (index - 1) / 2;
		if(heap->wakeups[parentIndex].time > heap->wakeups[index].time) {
			tmp = heap->wakeups[parentIndex];
			heap->wakeups[parentIndex] = heap->wakeups[index];
			heap->wakeups[index] = tmp;
			siftUp(heap, parentIndex);
		}
	}
}

//Reshuffling and reallocating items in the heap after removal.
void siftDown(WakeUpHeap* heap, int index) {
	int lChildIndex, rChildIndex, minIndex;
	WakeUp tmp;
	lChildIndex = 2 * index + 1;
	rChildIndex = 2 * index + 2;

	if(rChildIndex >= heap->size){
		if(lChildIndex >= heap->size)
			return;
		else
			minIndex = lChildIndex;
	}
	else {
		if(heap->wakeups[lChildIndex].time <= heap->wakeups[rChildIndex].time)
			minIndex = lChildIndex;
		else
			minIndex = rChildIndex;
	}
	if(heap->wakeups[index].time > heap->wakeups[minIndex].time) {
		tmp = heap->wakeups[minIndex];
		heap->wakeups[minIndex] = heap->wakeups[index];
		heap->wakeups[index] = tmp;
		siftDown(heap, minIndex);
	}

}

//Insert an item into the correct position of the heap
void insert(WakeUpHeap* heap, WakeUp item) {
	heap->size++;
	void * tmp = realloc(heap->wakeups, (heap->size*sizeof(WakeUp)));
	if(!tmp){
		perror("realloc");
		exit(-1);
	}	
	heap->wakeups = (WakeUp*)tmp;
	heap->wakeups[heap->size-1] = item;
	siftUp(heap, heap->size-1);
}

//Pop off the root item of the heap.
WakeUp removeMin(WakeUpHeap* heap) {
	if(heap->size == 0){ 
		fprintf(stderr, "Heap is empty, nothing to remove");
		exit(-1);
	}
	WakeUp min = heap->wakeups[0];
	heap->wakeups[0] = heap->wakeups[heap->size-1];
	heap->size--;
	void * tmp = realloc(heap->wakeups, (heap->size*sizeof(WakeUp)));
	
	heap->wakeups = (WakeUp*)tmp;
	siftDown(heap, 0);
	return min;
}


//On thread exit, print message
static void cleanExit(){
	printf("\nThread exited cleanly!\n");
}

//This thread announces the Wake up calls as they expire!
static void * Announcer(void *heap){
	
	pthread_cleanup_push(cleanExit, NULL);
	WakeUpHeap *thisheap = (WakeUpHeap *)heap;
	int expired = 0;
	struct timespec ts;
	int rt = 0;	
	
	/* Wait until there is an item in the thread available */
	while (thisheap->size == 0) {
		pthread_cond_wait(&thisheap->cond, &thisheap->lock);
	}
	while(1){
		
		//Pull top node off heap.
		WakeUp out = removeMin(thisheap);
		
		//Get the difference between alarms in seconds.
		time_t currentTime;
		currentTime = time(NULL);
		int diffTime = out.time - currentTime;
		clock_gettime(CLOCK_REALTIME, &ts);
		ts.tv_sec += diffTime;
		
		//add 1 to expired alarms counter.		
		expired += 1;

		//printf("\nThe Difference in time was %ds.\n",diffTime);			
		rt = pthread_cond_timedwait(&thisheap->cond, &thisheap->lock, &ts);
		if(rt == ETIMEDOUT){
			printf("\n---------------------------------");
			printf("\nWake up! %i %s", out.roomNo, ctime(&out.time));
			printf("---------------------------------\n");
			printf("Expired Alarms:    %i\n", expired);
			printf("Pending Alarms:    %i\n", thisheap->size);
			continue;
		}
		else{
			//insert later wakeUp back into heap.
			insert(thisheap, out);
			expired -= 1;
		}
		pthread_mutex_unlock(&thisheap->lock);
	}
	pthread_cleanup_pop(1);
}

//This thread Generates Wake up calls.
static void * WakeUp_Generator(void *heap){

	pthread_cleanup_push(cleanExit, NULL);
	WakeUpHeap *thisheap = (WakeUpHeap *)heap;
	
	
	while(1){
				
		//Pause for a random period up to 5 second.
		unsigned int a;
		usleep(rand_r(&a) % 5000000);
		
		time_t waketime;
		WakeUp call;

		//Generate a random room number.
		call.roomNo = rand_r(&a) % 5000;

		//Generate wake up call up to 100s in future.
		int random = rand_r(&a) % 100;
		waketime = time(NULL) + random;
		call.time = waketime;
	
		//Locking the mutex before adding to heap.	
		pthread_mutex_lock(&thisheap->lock);	
		if(thisheap->size == 0){
			//Insert Wakeup call into heap		
			insert(thisheap, call);
			printf("\nRegistering: %i %s \n", call.roomNo, ctime(&waketime));
			pthread_cond_signal(&thisheap->cond);
			
		}
		else if(call.time < thisheap->wakeups[0].time){
			//sending signal
			insert(thisheap, call);
			pthread_cond_signal(&thisheap->cond);
		}
		else{
			//Insert Wakeup call into heap		
			insert(thisheap, call);
			printf("\nRegistering: %i %s \n", call.roomNo, ctime(&waketime));
		}	
		pthread_mutex_unlock(&thisheap->lock);
	
	}
	pthread_cleanup_pop(1);
}  

int main(int argc, char *argv[]){
    
	//Initialising variables.
	pthread_t create,announce;
	WakeUpHeap heap;
	heap.wakeups = NULL;
	heap.size = 0;

	if(pthread_mutex_init(&heap.lock, NULL) != 0){
		printf("\nMutex init failed\n");
	}
	if(pthread_cond_init(&heap.cond, NULL) != 0){
		printf("\nCond init failed\n");
	}

	pthread_create(&create, NULL, WakeUp_Generator, &heap);
	pthread_create(&announce, NULL, Announcer, &heap);
	
	//This waits for the ctrl+c SIGINT and calls cleanups.
	sigset_t listen_sigs;
	sigemptyset(&listen_sigs);
	sigaddset(&listen_sigs, SIGINT);
	int listen_sig_r;
	
	pthread_sigmask(SIG_BLOCK, &listen_sigs, NULL);	
	sigwait(&listen_sigs, &listen_sig_r);

	//Freeing up everything.
	pthread_cancel(create);
	pthread_cancel(announce);

	pthread_join(create,NULL);
	pthread_join(announce,NULL);

	pthread_mutex_destroy(&heap.lock);
	pthread_cond_destroy (&heap.cond);

    printf("I hope you enjoyed your stay, Good Bye!");
	return 0;

}
