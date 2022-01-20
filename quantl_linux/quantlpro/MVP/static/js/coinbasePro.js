(()=>{
    // 
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    //Elements Init

    const cBKeyElement = document.querySelector("#cbProKey");
    const cBSecretElement = document.querySelector("#cbProSecret");
    const cBPassphraseElement = document.querySelector("#cbProPassphrase");
    const errorMessageElement = document.querySelector("#errorMessageCb");
    const cancelBtnElement =  document.querySelector("#cbProCancel");
    const loginBtnElement =  document.querySelector("#cbProLogin");
    const cbLabelElement = document.querySelector("#cbLabel");

    const cbConnectedBadge = document.querySelector("#cbConnectedBadge");
    const cbDisconnectBadge = document.querySelector("#cbDisconnectBadge");

    const successSnackbar = document.querySelector("#igSnackbar");
    const failureSnackbar = document.querySelector("#brokerConnectionFailure");

    const redirect_uri = 'http://127.0.0.1:8000/MVP/demo';
    const client_id = 'd60f6ca564e81060ba6e66a5af4331d3565faafd4fd1c36f8b4a7153034039ac';
    const client_secret = 'd455baddac7c52629d01426e9246ac25c90d3bb9677b2b8c346911476fb2e3cd';


    //Coinbase Oauth Implementation
    const coinbaseOAuth = () => {
        
        const defaultParams = {
            redirect_uri,
            client_id,
            client_secret
        };

        const base = 'https://www.coinbase.com/oauth/authorize?';

        const queryParams = {
            ...defaultParams,
            response_type: 'code',
            scope: 'wallet:accounts:read',
            state: '21093j21olnn21232paijerlerm213'
        }

        const coinbaseAuthEndpoint = base + toQueryString(queryParams);
        // window.open(coinbaseAuthEndpoint, 'Coinbase Authentication', 'height=300,width=300,left=375,top=330').focus();
        window.location.replace(coinbaseAuthEndpoint);

    }

    const getCoinbaseAccessToken = async (code) => {
        const queryParams = {
            grant_type: 'authorization_code',
            code,
            client_id,
            client_secret,
            redirect_uri,
        }
        console.log(toQueryString(queryParams));
        try{
            const authResp = await qhr.postWithQueryString('https://api.coinbase.com/oauth/token', queryParams);
            const authData = await authResp.data;
            console.log('Authorization data ', authData);
            return authData;
        }catch(err){
            console.trace('Error in fetching Coinbase access token', err);
            return {error: true}
        }
    }

    const getCoinbaseUser = async (accessToken) => {
        try{
            const userResp = qhr.getWithAuthBearer('https://api.coinbase.com/v2/user', accessToken);
            const userData = await userResp.data;
            console.log('Authorization data ', userData);
            return userData;
        }catch(err){
            console.trace('Error in fetching Coinbase user', err);
            return {error: true}
        }
    }


    // Rest Calls

    const connectCoinbase = async (data) => {
        try{ 
            const response = await qhr.post("/coinbase/connect_broker", data, csrftoken);
            const resData = await response.data;
            console.log("data from coinbase", resData);
            // const accountsData = resData["accounts"];
            if(!qtlStorage.getItem("CB") && resData){
                qtlStorage.storeItem("CB", resData["positions"]);
            }
            return resData["postions"];
        } catch(err){
            console.trace(`Error in connectCoinbase - ${err}`);
            failureSnackbar.className = "show";
                setTimeout(()=>{
                        failureSnackbar.className = failureSnackbar.className.replace("show", "");
                    },4000);
            
            return null;
        }   
    } 

    
    //If already logged in
    if(qtlStorage.getItem("CB")){
        const accountsData = qtlStorage.getItem("CB");
        console.log("Data from storage", accountsData);
        cbLabelElement.innerHTML = `Disconnect Coinbase`;
        cbConnectedBadge.style.visibility = "visible";
        cbConnectedBadge.style.display = "block";
    } 


    // Onclick Listeners

    loginBtnElement.onclick = () => {
        if(cBKeyElement.value.length > 0 && cBSecretElement.value.length > 0 && cBPassphraseElement.value.length > 0){
            errorMessageElement.style.visibility = "hidden";
            loginBtnElement.textContent = "Loading...";

            const coinBaseData = {key: cBKeyElement.value, secret: cBSecretElement.value, passphrase: cBPassphraseElement.value}; 
            // console.log(`Coinbase data -> ${coinBaseData}`);

            connectCoinbase(coinBaseData)
                .then((resp) => {
                    console.log(console.log("Checking Coinbase Accounts", JSON.parse(resp)));
                    cbLabelElement.innerHTML = `Disconnect Coinbase`;
                    cbConnectedBadge.style.visibility = "visible";
                    cbConnectedBadge.style.display = "block";
                    //Login Modal Close
                    loginBtnElement.textContent = "Login";
                    $("#connectCoinBaseModal").modal('hide');
                    //Clearing the inputs
                    cBKeyElement.value = "";
                    cBSecretElement.value = "";
                    cBPassphraseElement.value = "";

                    successSnackbar.className = "show";
                    setTimeout(()=>{
                            successSnackbar.className = successSnackbar.className.replace("show", "");
                        },4000);

                })
                .catch((err) => {
                    loginBtnElement.textContent = "Login"
                    cBKeyElement.value = "";
                    cBSecretElement.value = "";
                    cBPassphraseElement.value = "";
                    console.trace(`Error in connectCoinbase - ${err}`);
                    failureSnackbar.className = "show";
                    setTimeout(()=>{
                            failureSnackbar.className = failureSnackbar.className.replace("show", "");
                        },4000);
                });
            

            
            

        }else{
            errorMessageElement.style.visibility = "visible";
        }
    }


    //Cancel Btn onClick Listener -> Clear form
    cancelBtnElement.onclick = () => {
        cBKeyElement.value = "";
        cBSecretElement.value = "";
        cBPassphraseElement.value = "";
    }


    const disconnectCB = () =>{
        qtlStorage.removeItem("CB");
        cbLabel.innerHTML = `Coinbase`;
        cbConnectedBadge.style.visibility = "hidden";
        cbConnectedBadge.style.display = "none";
    }

    const clearUrl = () => {
        window.history.pushState({}, document.title, window.location.pathname);
        // let url = new URL(`${window.location.href}`);
        // let params = new URLSearchParams(url.search);
        // console.log(params);
        // params.delete('code');
        // params.delete('state');
    }
    
    //Onclick for coinbase tag in dropdown
    document.querySelector("#connectCb").onclick = () => {

        if(!qtlStorage.getItem("CB")){
            
            // $('#selectBrokersDropdown').dropdown('dispose');
            // $("#connectCoinBaseModal").modal('show');
            
              if(getParameterByName('code')){
                const code = getParameterByName('code');
                getCoinbaseAccessToken(code)
                .then((resp)=>{
                    console.log('AccessToken ready for getting user-> ', resp);
                    if(resp?.access_token){
                        getCoinbaseUser(resp["access_token"])
                        .then((resp)=>{
                            console.log("User from coinbase pro", resp)
                        })
                        .catch((err) => {
                            console.trace('Error ', err)
                        });
                    }
                    clearUrl();
                })
                .catch((err) => {
                    console.trace('Error in access token', err);
                    clearUrl();
                });
                
                    
              } else{
                    coinbaseOAuth();
              }
            
        } else {
            disconnectCB();
        }
        
        //for preventing default behaviour
        return false;
    }

    cbDisconnectBadge.onclick = () => {
        disconnectCB();
    }



})()






