
# coding: utf-8

# In[ ]:

from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute,IBMQ
import json 

def runQC():
    #IBMQ.enable_account('ENTER API TOKEN HERE')
    IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    nqubits = 5
    q = QuantumRegister(nqubits,'q')
    c = ClassicalRegister(nqubits,'c')
    circuit = QuantumCircuit(q,c)
    circuit.h(q) # Applies hadamard gate to all qubits
    circuit.measure(q,c) # Measures all qubits 
    '''backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= nqubits 
                                           and not x.configuration().simulator 
                                           and x.status().operational==True))'''

    backend = provider.get_backend('ibmq_qasm_simulator')
    print("least busy backend: ", backend)

    job = execute(circuit, backend, shots=1)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts(circuit)

    return counts


# In[ ]:

print(str(runQC()))


# In[ ]:

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    
    s = str(runQC())
    
    return s
app.run(host='0.0.0.0', port=50000)


# In[ ]:



