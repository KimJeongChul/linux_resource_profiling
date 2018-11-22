#!/usr/bin/python
import sys
import math

def cpu_workload(N):
    # Define CPU Workload
    # EXAMPLE math library
    for i in range(0, N):
        cos_i = math.cos(i)
        sin_i = math.sin(i)
        sqrt_i = math.sqrt(i)

def get_cpu_time():
    cpu_infos = {}
    with open('/proc/stat', 'r') as file_stat:
        """
        cpu : user nice system idle iowait irq softirq steal guest guest_nice
        cpu0 : ...
        idle_time = idle + iowait
        non_idle_time = user + nice + system + irq + softirq + steal
        total = idle_time + non_idle_time

        previous_total = previous_idle + previous_non_idle
        current_total = current_idle + current_non_idle
        diff_total = current_total - previous_total
        diff_idle = current_idle - previous_idle

        cpu_usage_percentage = ( diff_total - diff_idle )/ diff_total * 100
	"""
        cpu_lines = []
	for lines in file_stat.readlines():
            for line in lines.split('\n'):
                if line.startswith('cpu'):
                    cpu_lines.append(line.split(' '))
	for cpu_line in cpu_lines:
            if '' in cpu_line :
                cpu_line.remove('') # First row(cpu) exist '' and Remove ''
            cpu_id = cpu_line[0]
            user, nice, system, idle, iowait, irq, softriq, guest, guest_nice = [ float(item) for item in cpu_line[1:]]

            idle_time = idle + iowait
            non_idle_time = user + nice + system + irq + softirq + steal
            total = idle_time + non_idle_time

            cpu_infos.update({cpu_id : {'total' : total, 'idle' : idle_time }})
    return cpu_infos

def get_cpu_usage_percentage():
    start = get_cpu_time()
    cpu_workload(10 ** 6)
    end = get_cpu_time()

    cpu_usages = {}
    for cpu in start:
        diff_total = end[cpu]['total'] - start[cpu]['total']
        diff_idle = end[cpu]['idle'] - start[cpu]['idle']
        cpu_usage_percentage = (diff_total - diff_idle) / diff_total * 100
	cpu_usages.update({cpu : cpu_usage_percentage})
    return cpu_usages

def main():
    get_cpu_usage_percentage()

if __name__ == '__main__':
    main()
