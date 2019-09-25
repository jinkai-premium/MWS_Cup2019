from utils.search_malware import search_detect_malware, search_protect_action_taken

from pprint import pprint


def main():
    result = []
    result.extend(search_detect_malware())
    result.extend(search_protect_action_taken())

    pprint(result)


if __name__ == '__main__':
    main()
