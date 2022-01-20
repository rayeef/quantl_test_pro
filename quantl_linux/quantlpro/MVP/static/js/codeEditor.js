(()=>{
    // Retrieve Elements
    const executeCodeBtn = document.querySelector('.editor__run');
    const resetCodeBtn = document.querySelector('.editor__reset');
    const $editorConsole = document.querySelector('.editor__console');

    // constants
    const judge0Url = 'https://judge0-ce.p.rapidapi.com/submissions';
    const judge0Options = '?base64_encoded=true&fields=*';

    // default for python
    let language_id = 70 

    // Setup Ace
    let codeEditor = ace.edit("editorCode");
    let defaultCode = 'print("Quantl AI")';
    let defaultSettings = () => {
        var PythonMode = ace.require("ace/mode/python").Mode;
        codeEditor.session.setMode(new PythonMode());
    }
    let editorLib = {
        init() {
            // Configure Ace
            var PythonMode = ace.require("ace/mode/python").Mode;
            codeEditor.session.setMode(new PythonMode());
            
            // Set Options
            codeEditor.setOptions({
                fontFamily: 'Inconsolata',
                fontSize: '14pt',
                enableBasicAutocompletion: true,
                enableLiveAutocompletion: true,
            });
    
            // Set Default Code
            codeEditor.setValue(defaultCode);
        }
    }
    
    // Code Execution
    const createSubmission = async (userCode) => {
        // returns submission token
        const endpoint = judge0Url + judge0Options;
        const codeBase64 = btoa(userCode);
        // console.log('usercode to base 64',codeBase64);
        const data = {
            'language_id': language_id,
            'source_code': codeBase64,
            'stdin': "SnVkZ2Uw",
        }
        const token = await qhr.judge0Post(endpoint, data)
        .then(resp => {
            console.log("Response from judge0Post ->", resp);
            return resp;
        })
        .catch(err => {
            console.trace('Error in reaching judge0 while creating submission', err);
        });
        return token;
    }

    const getSubmission = async (token) => {
        // returns code result

        const endpoint = judge0Url + '/' + token + judge0Options;

        const executedResult = await qhr.judge0Get(endpoint)
        .then(resp => {
            // console.log("Response from judge0Get ->", resp);
            return resp;
        })
        .catch(err => {
            console.trace('Error in reaching judge0 while creating submission', err);
        });
        if(executedResult?.stderr){
            // console.log('compiled output in base64->', executedResult?.stderr);
            console.log(atob(executedResult?.stderr));
            return atob(executedResult?.stderr);
        }
        // console.log('compiled output in base64->', executedResult?.stdout);
        console.log(atob(executedResult?.stdout));

        return atob(executedResult?.stdout);
    }

    //Error handler 
    const errorOccurred = (err) => {
        executeCodeBtn.textContent = "Run";
        $editorConsole.textContent = err ? err : 'Error: Some Error Occured...';
    }

    const executeCode = (userCode) => {
        createSubmission(userCode)
            .then(resp => {
                // console.log('Response from creating submission', resp);
                getSubmission(resp?.token)
                .then(resp => {
                    // console.log('Response from getting the submission', resp);
                    executeCodeBtn.textContent = "Run";
                    $editorConsole.textContent = resp;
                })
                .catch(err => {
                    console.trace('Error in getting submission', err);
                    errorOccurred(err);
                });
            })
            .catch(err => {
                console.trace('Error in creating submission', err);
                errorOccurred(err);
            });
    } 

    // Events
    executeCodeBtn.addEventListener('click', () => {
        // Get input from the code editor
        const userCode = codeEditor.getValue();

        // Run the user code
        try {
            // new Function("console.log('Hi Quantl')")();
            // console.log("Users code from execute button", userCode);
            executeCodeBtn.textContent = "Running...";
            executeCode(userCode);

        } catch (err) {
            console.error(err);
        }
    });

    resetCodeBtn.addEventListener('click', () => {
        // Clear ace editor
        codeEditor.setValue(defaultCode);
    })

    editorLib.init();

})()


