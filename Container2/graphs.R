library(lattice)

read.table("output-throughput-latency/stats.csv", header=TRUE) -> csvDataFrameSource
csvDataFrame <- csvDataFrameSource

trellis.device("pdf", file="graph1.pdf", color=T, width=6.5, height=5.0)

# ... xyplot here

xyplot(requests ~ rate, data=csvDataFrame, type='l')


dev.off() -> null 

trellis.device("pdf", file="graph2.pdf", color=T, width=6.5, height=5.0)

# ... xyplot here
xyplot(latency ~ responses, data=csvDataFrame, type='l')

dev.off() -> null 
