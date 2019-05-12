import csv
import silk

test_file = "/home/jwc3f/silk/GIGAMON-NF-1/inweb/2017/06/01/iw-GIGAMON-NF-1_20170601.00"
out_file = "out.csv"

def id_from_record(rec):
  return (rec.sip, rec.dip, rec.sport, rec.dport, rec.protocol)

class TcpTrace:
  def __init__(self, list_of_flows):
    sample_record = list_of_flows[0][0]
    # Identifying elements
    self.protocol = sample_record.protocol
    self.srcIp = sample_record.sip
    self.srcPort = sample_record.sport
    self.dstIp = sample_record.dip
    self.dstPort = sample_record.dport
    # Computed features
    self.startTime = sample_record.stime_epoch_secs
    self.endTime = sample_record.stime_epoch_secs + sample_record.duration_secs
    self.bytes = 0
    self.packets = 0
    self.flowLength = 0
    self.recordLength = 0
    for flow in list_of_flows:
      self.flowLength += 1
      for rec in flow:
        self.recordLength += 1
        self.packets += rec.packets
        self.bytes += rec.bytes
        startTime = rec.stime_epoch_secs
        self.startTime = min(self.startTime, startTime)
        endTime = rec.stime_epoch_secs + rec.duration_secs
        self.endTime = min(self.endTime, endTime)

  def data(self):
    return [self.srcIp, self.dstIp, self.srcPort, self.dstPort, self.protocol,
      self.startTime, self.endTime, self.bytes, self.packets, self.flowLength, self.recordLength]

def TcpTraceDataHeaders():
  return ['srcIp', 'dstIp', 'srcPort', 'dstPort', 'protocol', 'startTime', 'endTime', 'bytes', 'packets',
    'flowLength', 'recordLength']

__limit = 1*10**10
def main():
  myfile = silk.SilkFile(test_file, silk.READ)
  print "file", myfile

  protocol_counts = {}
  rec_count = 0
  flows_by_id = {}

  # 0. Iterate through Netflow records
  for rec in myfile:
    rec_count += 1
    if rec_count > __limit: break

    # (0.1. Count protocols.)
    prot = rec.protocol
    if prot not in protocol_counts:
      protocol_counts[prot] = 0
    protocol_counts[prot] += 1
    
    # 1. Track flows
    record_id = id_from_record(rec)
    if record_id not in flows_by_id:
      flows_by_id[record_id] = []
    flows_by_id[record_id].append(rec)

  # 3. Break flows up into lines by SYN and FYN records
  trace_lines_by_id = {}
  for record_id in flows_by_id:
    flow = flows_by_id[record_id]
    trace = None
    for record in flow:
      tcp_flags = record.tcpflags
      start_flag = tcp_flags.syn 
      end_flag = tcp_flags.fin or tcp_flags.rst
      if start_flag:
        trace = [record]
      if end_flag:
        if trace:
          if not start_flag:
            trace.append(record)
          record_id = id_from_record(record)
          if record_id not in trace_lines_by_id:
            trace_lines_by_id[record_id] = []
          trace_lines_by_id[record_id].append(trace)
      if not (start_flag or end_flag):
        if trace:
          trace.append(record)

  # 4. Separate flows by timestamp
  flow_lines = []
  for flow_id in trace_lines_by_id:
    flow_lines.append(trace_lines_by_id[flow_id])

  # 5. Compute traces from lines of flows
  traces = [TcpTrace(flow_list) for flow_list in flow_lines]

  # 6. Export traces to CSV
  with open(out_file, 'w') as csv_file:  
     writer = csv.writer(csv_file)
     writer.writerow(TcpTraceDataHeaders())
     tracedata = [trace.data() for trace in traces]
     writer.writerows(tracedata)

print TcpTraceDataHeaders()
main()
