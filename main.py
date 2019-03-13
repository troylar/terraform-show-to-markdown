import click
from report import ReportGenerator

@click.command()
@click.argument('report_file')
@click.argument('unique_id', required=True)
def main(report_file, unique_id):
    r = ReportGenerator(ReportFile=report_file, UniqueId=unique_id)
    r.import_data()
    r.generate()

if __name__ == '__main__':
    main()
