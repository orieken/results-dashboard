import json
import sys
import requests
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description='Process test results and post them to a service.', add_help=False)
    parser.add_argument('framework', type=str, nargs='?', help='The testing framework (behave or pytest)')
    parser.add_argument('file', type=str, nargs='?', help='The JSON result file')
    parser.add_argument('--usage', action='store_true', help='Show usage information and exit')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                        help='Show this help message and exit')
    return parser.parse_args()


def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def process_behave(data):
    results = {'passing': 0, 'failing': 0, 'pending': 0}
    for feature in data:
        for element in feature['elements']:
            if element['status'] == 'passed':
                results['passing'] += 1
            elif element['status'] == 'failed':
                results['failing'] += 1
            else:
                results['pending'] += 1
    return results


def process_pytest(data):
    results = {
        'passing': data['summary']['passed'],
        'failing': data['summary']['failed'],
        'pending': data['summary']['total'] - data['summary']['passed'] - data['summary']['failed']
    }
    return results


def process_cucumberjs(data):
    results = {'passing': 0, 'failing': 0, 'pending': 0}
    for feature in data:
        for element in feature['elements']:
            for step in element['steps']:
                if 'result' in step:
                    if step['result']['status'] == 'passed':
                        results['passing'] += 1
                    elif step['result']['status'] == 'failed':
                        results['failing'] += 1
                    elif step['result']['status'] == 'undefined':
                        results['pending'] += 1
    return results


def create_payload(name, results):
    return {
        "name": name,
        "results": results
    }


def post_results(url, payload):
    response = requests.post(url, json=payload)
    return response.status_code


def show_usage():
    print("""
Usage: python test_results_cli.py [OPTIONS] FRAMEWORK FILE

Arguments:
  FRAMEWORK  The testing framework to process ('behave', 'pytest', or 'cucumberjs').
  FILE       The path to the JSON result file.

Options:
  --usage    Show this message and exit.
  -h, --help Show help message and exit.
""")


def main():
    args = parse_args()

    if args.usage:
        show_usage()
        sys.exit(0)

    data = read_json(args.file)
    name = args.file.split('.')[0]

    if args.framework == 'behave':
        results = process_behave(data)
    elif args.framework == 'pytest':
        results = process_pytest(data)
    elif args.framework == 'cucumberjs':
        results = process_cucumberjs(data)
    else:
        print("Unsupported framework")
        sys.exit(1)

    payload = create_payload(name, results)
    status_code = post_results('http://127.0.0.1:5000/teams', payload)

    if status_code in (200, 201):
        print("Data posted successfully.")
    else:
        print(f"Failed to post data. Status code: {status_code}")


if __name__ == "__main__":
    main()
