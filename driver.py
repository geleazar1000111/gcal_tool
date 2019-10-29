import csv
import gcal_tool


def main():
    while 1:
        try:
            max_results = int(input("Please enter the number of events you would like to get: "))
            assert isinstance(max_results, int)
            assert 1 <= max_results <= 2500
            break
        except ValueError:
            print("Incorrect form of input (must be int)")
        except AssertionError:
            print("Integer must between 1 and 2500")
    event_list = gcal_tool.create_event_color_list(max_results)
    if event_list:
        with open('gcal_tool_results', 'w', newline='') as csvfile:
            gcal_writer = csv.writer(csvfile)
            gcal_writer.writerow(
                ["Event name"] + ["Color"] + ["Start"] + ["End"] + ["Time spent (hours)"])  # + ["Time free (hours)"])
            for event in event_list:
                gcal_writer.writerow(event)
        csvfile.close()


if __name__ == '__main__':
    main()
