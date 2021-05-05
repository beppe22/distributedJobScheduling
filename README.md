# distributedJobScheduling

Below the description of the project's requests

"Implement an infrastructure to manage jobs submitted to a cluster of Executors. Each client may submit a job to any of the executors receiving a job id as a return value. Through such job id, clients may check (contacting the same executor they submitted the job to) if the job has been executed and may retrieve back the results produced by the job.
Executors communicate and coordinate among themselves in order to share load such that at each time every Executor is running the same number of jobs (or a number as close as possible to that). Assume links are reliable but processes (i.e., Executors) may fail (and resume back, re-joining the system immediately after).
Choose the strategy you find more appropriate to organize communication and coordination. Use stable storage to cope with failures of Executors.
Implement the system in Java (or any other language you choose) only using basic communication facilities (i.e., sockets and RMI, in case of Java). Alternatively, implement the system in OMNeT++, using an appropriate, abstract model for the system (including the jobs themselves)."
