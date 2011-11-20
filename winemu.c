//A GENUINE WINDOWS EMULATOR

#include <stdio.h>
#include <unistd.h>

int main(void)
{
	char buf;
	
	printf("[0m[2J[1;1H[22;25;24;44m                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                   [34;47m Windows [44mws[37m                                  "
"                                                                                "
"[1m       An exception 0E has occurred at 0028:C0018DBA in VxD IFSMGR(01) +        "
"       0000340A.  This was called from 0028:C0034118 in VxD NDIS(01) +          "
"       00000D7C.  It may be possible to continue normally.                      "
"                                                                                "
"       *  Press any key to attempt to continue                                  "
"       *  Press CTRL+ALT+DEL to restart your computer. You will                 "
"          lose any unsaved information in all applications                      "
"                                                                                "
"                           Press Any key to continue.                           "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"                                                                                "
"[0m");
	fflush(stdout);
	read(0, &buf, 1);
	return 0;
}
