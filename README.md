# QMASM Docker

This repo hosts a dockerised version of the excellent [QMASM](https://github.com/lanl/qmasm) Quantum Macro Assembler from Scott Pakin.

## Setup and run

Given that docker is installed and that you are at the root of the cloned repo:

```bash
# build the image
docker build -t qmasm-rest --rm .
# run the image, listening to port 80 on the host
docker run -d -p 80:80 --name qmasm-rest qmasm-rest
```

Or using the scripts:
```bash
./build_image.sh
./run_image.sh
```

## Usage

The server has a unique endpoint. It accepts POST requests with a `.qmasm` file content in the body. By default, the server will run `qmasm` with the following arguments:

```bash
qmasm --format="qbsolv" --values="ints" "<QMASM BODY>"
```

To pass other arguments to QMASM, simply specify them as _query parameters_. 

__Important__: 

* options with no values (for example `--run`) should have a trailing `=` (for example `run=`);
* omit the slashes before the options, they will be added automatically.

### Examples using CURL

```bash
# run "qmasm --help"
curl "http://localhost?help"

# run "qmasm -q --run somefile.qmasm"
curl -H 'Content-Type: text/plain' \
     --data-binary "@somefile.qmasm" \
     "http://localhost/?run=&q=" > somefile.qmasm.out

# run "qmasm --format=qubist --run somefile.qmasm"
curl -H 'Content-Type: text/plain' \
     --data-binary "@somefile.qmasm" \
     "http://localhost/?format=qubist&run=" > somefile.qmasm.out

# translate the qmasm file into a qbsolv (.qubo) format "qmasm --format=qbsolv"
curl -H 'Content-Type: text/plain' \
      --data-binary "@somefile.qmasm" \
      "http://localhost/?format=qbsolv" > somefile.qubo
```

### Examples using Python3

Here, we use the [requests](http://docs.python-requests.org/en/master/) library to make HTTP calls.

```python3

def call_qmasm(qmasm_input: str, host='http://localhost', **params) -> str:
    """
    run qmasm in "qbsolv" mode.
    :param qmasm_input: the input for qmasm
    :param params: options to pass to qmasm
    :return: the output of qmasm
    """
    default_params = dict(run='')
    default_params.update(params)
    resp = requests.post(host, qmasm_input, params=default_params)
    output = resp.text
    if resp.status_code != 200:
        raise Exception("qmasm failed: %s" % output)
    return output

with open('somefile.qmasm') as f:
    qmasm_input = f.read()

# run qmasm --format=qbsolv --values=int --run "somefile.qmasm"
output = call_qmasm(qmasm_input)

# run qmasm --format=qubist --values=int -q --run "somefile.qmasm"
# note the q='', this is how you encode options with no values
output = call_qmasm(qmasm_input, format=qubist, q='')
```
