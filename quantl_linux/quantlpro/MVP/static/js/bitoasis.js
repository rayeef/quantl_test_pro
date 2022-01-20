(()=>{
    // 
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    //Elements Init
    const $bitoasisLabel = document.querySelector("#bitoasisLabel");
    const $apiKey = document.querySelector("#bitoasisKey");
    const $errorMessage = document.querySelector("#errorMessageBitoasis");
    const $cancelBtn =  document.querySelector("#bitoasisCancel");
    const $loginBtn =  document.querySelector("#bitoasisLogin");

    const $bitoasisConnectedBadge = document.querySelector("#bitoasisConnectedBadge");
    const $bitoasisDisconnectBadge = document.querySelector("#bitoasisDisconnectBadge");
   
    const $successSnackbar = document.querySelector("#igSnackbar");
    const $failureSnackbar = document.querySelector("#brokerConnectionFailure");

    // const $bitoasisDataView = document.querySelector('#bitoasisDataView');
    const $emptyBrokerView = document.querySelector('#emptyBrokerView');

    // Rest Calls

    const connectBitoasisApi = async (data) => {
        try{ 
            const response = await qhr.post("/bitoasis/connect_broker", data, csrftoken);
            const resData = await response.data;
            // console.log("Data in connect bitoasis api", resData)
            const accountData = resData["checkTrades"];
            return accountData;
        } catch(err){
            console.trace(`Error in connectBitoasis - ${err}`);
            $("#connectBitoasisModal").modal('hide');
            $failureSnackbar.className = "show";
            setTimeout(()=>{
                    $failureSnackbar.className = $failureSnackbar.className.replace("show", "");
                },4000);
            
            return null;
        }   
    } 

    const connectSuccess = (data) => {
        let accountData = JSON.parse(data)
        console.log(console.log("Checking Bitoasis Trades", accountData)); 

        if(!qtlStorage.getItem("BO") && accountData){
            qtlStorage.storeItem("BO", accountData);
        } 
        $bitoasisLabel.innerHTML = `Disconnect Bitoasis`;
        $bitoasisConnectedBadge.style.display = "block";
        // $emptyBrokerView.style.display = "none";
        //Login Modal Close
        $loginBtn.textContent = "Login";
        $("#connectBitoasisModal").modal('hide');
        //Clearing the inputs
        $apiKey.value = "";

        $successSnackbar.className = "show";
        setTimeout(()=>{
                $successSnackbar.className = $successSnackbar.className.replace("show", "");
            },4000);

    }

    const connectFailure = (err) => {
        $loginBtn.textContent = "Login"
        $apiKey.value = "";
        console.trace(`Error in connectBitoasis - ${err}`);
        $("#connectBitoasisModal").modal('hide');
        $failureSnackbar.className = "show";
        setTimeout(()=>{
                $failureSnackbar.className = $failureSnackbar.className.replace("show", "");
            },4000);

    }
    
    //If already logged in
    if(qtlStorage.getItem("BO")){
        const accountsData = qtlStorage.getItem("BO");
        console.log("Data from local storage Bitoasis", accountsData);
        $bitoasisLabel.innerHTML = `Disconnect Bitoasis`;
        $bitoasisConnectedBadge.style.display = "block";
    }else{
        // $bitoasisDataView.style.display = "none";
        if(!qtlStorage.getItem("CB") && !qtlStorage.getItem("IG") && !qtlStorage.getItem("BN")){
            $emptyBrokerView.style.display = "flex";
        }
    }

    // Onclick Listeners

    $loginBtn.onclick = () => {
        if($apiKey.value.length > 0){
            $errorMessage.style.visibility = "hidden";
            $loginBtn.textContent = "Loading...";

            const bitoasisData = {key: $apiKey.value}; 
            console.log(`Bitoasis data from frontend -> `,bitoasisData);

            try{
                const connectBitoasis = async () => {
                    const data = await connectBitoasisApi(bitoasisData);
                    // console.log("Data from connectBitoasisApi", data);
                    if(data){
                        connectSuccess(data);
                    }else if(!data){
                        connectFailure('Error: Data from connectBitoasisApi not handled correctly !')
                    }
                }
                connectBitoasis();
                
            } catch(err){
                connectFailure(err);
            }

        }else{
            $errorMessage.style.visibility = "visible";
        }
    }

    // Cancel Btn onClick Listener -> Clear form
    $cancelBtn.onclick = () => {
        $apiKey.value = "";
    }


    const disconnectBitoasis = () => {
        qtlStorage.removeItem("BO");
        $bitoasisLabel.innerHTML = `Bitoasis`;
        $bitoasisConnectedBadge.style.display = "none";
        // $bitoasisDataView.style.display = "none";
        if(!qtlStorage.getItem('CB') && !qtlStorage.getItem('IG') && !qtlStorage.getItem('BN')){
            $emptyBrokerView.style.display = "flex";
        }
    }

    //Onclick for coinbase tag in dropdown
    document.querySelector("#connectBitoasis").onclick = () => {
        if(!qtlStorage.getItem("BO")){
            $('#selectBrokersDropdown').dropdown('dispose');
            $("#connectBitoasisModal").modal('show');
        } else {
            disconnectBitoasis();
        }
        //for preventing default behaviour
        return false;
    }

    $bitoasisDisconnectBadge.onclick = () => {
        disconnectBitoasis();
    }

})()






