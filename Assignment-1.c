#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>

/*
This assignment reads in a file and alternating threads 
print alternating words.
*/

//Define structure to pass arguments to thread.
typedef struct {
	char name;
	pid_t *pid;
	FILE *fp;
} t_args;

//On thread exit, print message
static void cleanExit(void *arg){
	t_args *args = (t_args *)arg;
	printf("Thread %c exited cleanly!\n", args->name);
}

//Function to be run by threads.
static void * threadHandler(void *p_args){
	pthread_cleanup_push(cleanExit, p_args);
	t_args *args = (t_args *)p_args;
    
    //Allocating maximum word size in heap memory.
	char *s = malloc(64); 
    unsigned int seed;

    //Creating a sigset to block and blocking it.
	sigset_t block_sigs;
	sigaddset(&block_sigs, SIGUSR1);
	sigaddset(&block_sigs, SIGUSR2);
	pthread_sigmask(SIG_BLOCK, &block_sigs, NULL);

    //Create a sigset for sigwait to listen for.
	sigset_t listen_sigs;
	sigemptyset(&listen_sigs);
	sigaddset(&listen_sigs, SIGUSR1);
	int listen_sig_r;
	
	//Main reading loop.
	while(1){
        //Awaits signal from main to begin single word read.
		sigwait(&listen_sigs, &listen_sig_r);
		if(fscanf(args->fp, "%s", s) == EOF) {
        	kill(*args->pid, SIGUSR2);
			continue;
		}
        //Pause for a random period up to 1 second.
        usleep(rand_r(&seed) % 1000000);
		//Print read word.
        printf("Thread %c: %s \n", args->name, s); 	
        //Signal main thread that read is complete.
        kill(*args->pid, SIGUSR2);
	}
    //Free allocated memory and run clean up function.
	free(s);
    pthread_cleanup_pop(1);
}

int main(int argc, char *argv[]){
    
    //Initialise threads
    pthread_t a, b;
	t_args args_a, args_b;

	FILE *fp;
	char in;
	pid_t pid;
    
	if(argc < 2) {
		printf("Usage: %s file \n", argv[0]);
		return 1;
	}
    
    fp = fopen(argv[1], "r");
	if(fp == NULL){
		perror("fopen");
		return 1;
	}

	pid = getpid();

	args_a.name = 'A';
	args_a.fp = fp;
	args_a.pid = &pid;
	
	args_b.name = 'B';
	args_b.fp = fp;
	args_b.pid = &pid;

    //Block all signals
	sigset_t block_sigs;
	sigaddset(&block_sigs, SIGUSR1);
	sigaddset(&block_sigs, SIGUSR2);

	pthread_sigmask(SIG_BLOCK, &block_sigs, NULL);
	
	//Create a listen set for SIGCONT so we know when to continue
	sigset_t listen_sigs;
	sigemptyset(&listen_sigs);
	sigaddset(&listen_sigs, SIGUSR2);
	int listen_sig_r;

	pthread_create(&a, NULL, threadHandler, (void *) &args_a);
    pthread_create(&b, NULL, threadHandler, (void *) &args_b);


    while(1) {	
		if(feof(fp))
            break;
        pthread_kill(a, SIGUSR1);
		sigwait(&listen_sigs, &listen_sig_r);

        if(feof(fp))
            break;
        pthread_kill(b, SIGUSR1);
		sigwait(&listen_sigs, &listen_sig_r);
	}

    pthread_cancel(a);
    pthread_cancel(b);
	pthread_join(a, NULL);			
	pthread_join(b, NULL);			

	fclose(fp);
	return(0);
}

