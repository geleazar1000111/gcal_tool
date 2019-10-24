import csv
import gcal_tool


def main():
    event_map = gcal_tool.create_event_color_map()

    with open('gcal_tool_results', 'w', newline='') as csvfile:
        gcal_writer = csv.writer(csvfile)
        gcal_writer.writerow(["Event name"] + ["Color"] + ["Start"] + ["End"] + ["Time spent (hours)"] + ["Time free (hours)"])
        for key in event_map:
            gcal_writer.writerow([key] + event_map[key])
    csvfile.close()

if __name__ == '__main__':
    main()
