all:
	python3.6 run_assignment1.py --input_path 'assignment_1_data/input.json' --solution_path 'results/solution.json'
	python3.6 error_check.py --ground_truth_path 'assignment_1_data/output.json' --solution_path 'results/solution.json' --error_path 'results/error_list.json'
	python3.6 format_checker.py --solution_path 'results/solution.json' --ground_truth 'assignment_1_data/output.json'