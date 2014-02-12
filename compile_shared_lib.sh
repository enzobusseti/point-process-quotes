gcc -g -O0 -std=gnu99 -Wall -Wfloat-equal -Wtype-limits -Wpointer-arith -Wlogical-op -fno-diagnostics-show-option -fPIC -c scalar_log_likelihood.c
gcc -shared -o scalar_log_likelihood.so scalar_log_likelihood.o
