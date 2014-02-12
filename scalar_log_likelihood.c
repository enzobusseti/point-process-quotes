#include "math.h"
#include "float.h"
#include "stdlib.h"
#include "stdio.h"

/* Data is a list of arrays of doubles. Each one of these arrays
    is the time series of events of a particular type. 
    Lambda_0 is a scalar. Alpha and beta
    are M-vectors. length_time_series are the lenght of each element of data[],
    number_event_types is the number of different event types,
    event_type is the particular event type for which we compute the log lik.

    I FOLLOW THE DERIVATION OF THE USUAL HAWKES SLIDES*/

char * LOG_FILE = "c_loglik.log";
    
double _scalar_loglik(int number_event_types, double * data[], int length_time_series[], 
	int event_type, double lambda_0, double alpha[], double beta[]){

	//FILE * logfile = fopen(LOG_FILE, "a");
	//printf("Starting loglik function\n");
	//printf("lambda_0 = %f, alpha = %f, %f, beta = %f, %f\n", lambda_0, alpha[0], alpha[1], beta[0], beta[1]);
	//printf("length_time_series = %d, %d\n", length_time_series[0],length_time_series[1]);

	printf("event_type = %d\n", event_type);

	//printf("number_event_types = %d\n", number_event_types);
	//printf("Slice of data: data[0][0] = %f, data[0][-1] = %f\n", //, data[1][0] = %f, data[1][-1] = %f\n",
	//	**data, *(*data + length_time_series[0]-1));//, **(data+1), *(*(data+1) + length_time_series[1]-1));


	/*Find the smallest and maximum time in all the series we have.*/
	double end_time = 0.;
	double start_time = FLT_MAX;

	for (int i = 0; i < number_event_types; i++){
		if (length_time_series[i] == 0) continue;
		if (*(*(data+i) + length_time_series[i]-1) > end_time) end_time = *(*(data+i) + length_time_series[i]-1);
		if (*(*(data+i) + 0) < start_time) start_time = *(*(data+i) + 0);
	}

	//printf("start_time = %f, end_time = %f\n", start_time, end_time);

	/*Start building the result.*/
	double result = end_time;

	/* this passage is right, I think. 
	In the slides it's wrong. I derived it myself (also by analogy with the 1D case) */
	result = result - lambda_0 * (end_time - start_time); 

	/* Keep following the slides. */
	for (int i = 0; i < number_event_types; i++){
		for (int j = 0; j < length_time_series[i]; j++){
			result = result - (1 - exp(-beta[i] * (end_time - (*(data+i))[j]))) * alpha[i]/beta[i];
		}
	}

	/* Now compute R, the real hard part.
	I define counters for resuming iteration
	over the various event types. */
	int counters[number_event_types];

	/* I never store the whole sequence of values of R. 
	Only keep the most recent value (to use in the recursive def.)
	and update the result one iteration at a time. */
	double R_vector[number_event_types];

	/*Initial values.*/
	for (int i = 0; i < number_event_types; i++){
		counters[i] = 0;
		R_vector[i] = 0.;
	};

	double last_time_threshold = *(*(data+event_type));; // holds the last time of event of type m

	//printf("Initial time: %f\n", last_time_threshold);

	/*Iterate over the time series of events of type m*/
	for (int j = 0; j < length_time_series[event_type]; j++){

		// we need to sum over events before this threshold
		double current_time_threshold = *(*(data+event_type)+j);

		// we'll use the time elapsed b/w last two events in the computation
		double time_diff = current_time_threshold - last_time_threshold; 
		last_time_threshold = current_time_threshold;
		
		//iterate over all event types
		for (int i = 0; i < number_event_types; i++){

			//if the event is the one we study we have a special case
			if (i == event_type && j > 0) //j > 0 to account for first iteration
				R_vector[i] = exp(-beta[i]*time_diff) * (1 + R_vector[i]);
			else {
				R_vector[i] = R_vector[i] * exp(-beta[i]*time_diff);
				for (counters[i]; counters[i] < length_time_series[i]; counters[i]++){
					if ((*(data+i))[counters[i]] > current_time_threshold) break;
					R_vector[i] += exp(-beta[i] * (current_time_threshold -  (*(data+i))[counters[i]]));
				}
			}
		}

		/* All the values of R have been updated. Use them for the result.*/
		double R_sums = 0.;
		for (int i = 0; i < number_event_types; i++){
			R_sums += alpha[i] * R_vector[i];
		} 

		//printf("R_sums = %f\n", R_sums);

		result = result + log(lambda_0 + R_sums);
	}

	//printf("C result = %f\n", result);
	//fclose(logfile);

	return result;

} 

int main(int argc, char * argv[]){
	int number_event_types = 2;
	double *data[2];

	double data_0_stack[3] = {3.,5.,7.};
	data[0] = data_0_stack;

	double data_1_stack[4] = {1.,4.,10.,12.};
	data[1] = data_1_stack;

	int length_time_series[2] = {3,4};
	int event_type = 0;
	double lambda_0 = 1.; 
	double alpha[2] = {1,1};
	double beta[2] = {1,1};

	printf("Result: %f\n", _scalar_loglik(number_event_types, data, length_time_series, event_type, lambda_0, alpha, beta));
	return 0;
}