# Rachit Jain | 2018ME10032 | COL772 | A1 | Prof. Mausam | Deadline: 11th September 2021
# Creating a rule-based model used to convert written speech to spoken text

## This file is to check the percentage error in the number of terms mapped to their token according to the conditions mentioned in the problem statement


## Importing necessary libraries
import json
import argparse


## Returns a dictionary mapping every SID with its corresponding error percentage
def error_calculator(output_data, solution_data):
    error_list = {}
    count = 0
    percentage_error = 0
    total_perc_error = 0

    for output_sentence in output_data:
        res_sid = output_sentence['sid']
        res_token = output_sentence['output_tokens']

        sol_token  = solution_data[res_sid]['output_tokens']
        for i in range(len(res_token)):
            # print(res_sid)
            if (res_token[i] != sol_token[i]):
                count += 1
        percentage_error = 100*count/len(res_token)
        total_perc_error += percentage_error
        error_list[res_sid] = percentage_error
        count = 0

    final_error = total_perc_error/len(error_list)
    error_list['total'] = final_error
    print("Total Error: ", final_error)
    return error_list


if __name__ == '__main__':

    ## Argument Parser
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--ground_truth_path', required=True, help='Ground Truth Labeled File Path')
    arg_parser.add_argument('--solution_path', required=True, help='Solution File Path')
    arg_parser.add_argument('--error_path', required=True, help='Error File Path')

    args = arg_parser.parse_args()


    ## Importing output data.
    with open(args.ground_truth_path,'r', encoding='utf8') as output_file:
        output_data = json.load(output_file)
        output_file.close()

    ## Importing the file that contained results we created using our code.
    with open(args.solution_path,'r', encoding='utf-8') as solution_file:
        solution_data = json.load(solution_file)
        solution_file.close()

    ## Running the error calculator.
    error_list = error_calculator(output_data, solution_data)

    ## Saving the errors in a file.
    with open(args.error_path,'w') as error_file:
        json.dump(error_list, error_file, indent=2, ensure_ascii=False)
        error_file.close()