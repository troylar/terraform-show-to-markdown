from report import ReportGenerator

r = ReportGenerator(ReportFile="./test/test2.data")
r.import_data()
r.generate()
