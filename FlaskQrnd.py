
# coding: utf-8

# In[ ]:

from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, execute,IBMQ
import json 

IBMQ.enable_account('983b7e03809ecbd0c79e68f8cd52cdaff7426519e8c72a6dfd47d2297415d60b2850c213de650c4b79bc835d7a22939683a472b184d851344833965a426f7c5f')

def runQC():
    #IBMQ.enable_account('983b7e03809ecbd0c79e68f8cd52cdaff7426519e8c72a6dfd47d2297415d60b2850c213de650c4b79bc835d7a22939683a472b184d851344833965a426f7c5f')
    #IBMQ.load_account()
    provider = IBMQ.get_provider(hub='ibm-q')
    nqubits = 5
    q = QuantumRegister(nqubits,'q')
    c = ClassicalRegister(nqubits,'c')
    circuit = QuantumCircuit(q,c)
    circuit.h(q) # Applies hadamard gate to all qubits
    circuit.measure(q,c) # Measures all qubits 
    backend = least_busy(provider.backends(filters=lambda x: x.configuration().n_qubits >= nqubits 
                                           and not x.configuration().simulator 
                                           and x.status().operational==True))

    #backend = provider.get_backend('ibmq_qasm_simulator')
    print("least busy backend: ", backend)

    job = execute(circuit, backend, shots=1)
    #job_monitor(job)
    result = job.result()
    counts = str(result.get_counts(circuit))

    return counts + " from " + str(backend)


# In[ ]:

#print(str(runQC()))


# In[ ]:

from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    
    s = str(runQC())
    
    return s
app.run(host='0.0.0.0', port=50000)


# In[ ]:



