// const worker = new Worker(js_ig_worker);

const $igDataView = document.querySelector('#igDataView');
const $emptyBrokerView = document.querySelector('#emptyBrokerView');

//HTML Elements
const pl1Element = document.querySelector("#pl1");
const acc1 = document.querySelector("#acc1");
const acc1Blnc = document.querySelector("#acc1Blnc");
const acc2 = document.querySelector("#acc2");
const acc2Blnc = document.querySelector("#acc2Blnc");
const acc1Blnc1 = document.querySelector("#acc1Blnc1");
const pl1_1 = document.querySelector("#pl1-1");
const igLabel = document.querySelector("#igLabel");

const errorMessage = document.querySelector("#errorMessageIg");
const igConnectedBadge = document.querySelector("#igConnectedBadge");
const igDisconnectBadge = document.querySelector("#igDisconnectBadge");


//Populating the data with local storage
if(qtlStorage.getItem("IG")){
    const accountsData = qtlStorage.getItem("IG");
    pl1Element.innerHTML += `${accountsData["pl1"]}`;
    pl1_1.innerHTML += `${accountsData["pl1"]}`;
    acc1.innerHTML += `${accountsData["account_1"]}`;
    acc1Blnc.innerHTML += `${accountsData["account_1_balance"]}`;
    acc1Blnc1.innerHTML += `${accountsData["account_1_balance"]}`;
    acc2.innerHTML += `${accountsData["account_2"]}`;
    acc2Blnc.innerHTML += `${accountsData["account_2_balance"]}`;
    igLabel.innerHTML = `Disconnect IG`;
    igConnectedBadge.style.visibility = "visible";
    igConnectedBadge.style.display = "block";
}else {
    $igDataView.style.display = "none";
    if(!qtlStorage.getItem("CB") && !qtlStorage.getItem("BN")){
        $emptyBrokerView.style.display = "flex";
    }
}


//Cancel Btn onClick Listener -> Clear form
document.querySelector("#connectBrokerCancel").onclick = () => {

    document.querySelector("#connectBrokerId").value = "";
    document.querySelector("#connectBrokerPwd").value = "";

}

//Login Btn onClick Listener
document.querySelector("#connectBrokerLogin").onclick = () => {

    const cBId = document.querySelector("#connectBrokerId").value;
    const cBPwd = document.querySelector("#connectBrokerPwd").value;
    const cBApiKey = document.querySelector("#connectBrokerApi").value;
    const cBAT = document.querySelector("#connectBrokerAT").value
    // console.log(`Login Id ${cBId} Password ${cBPwd} Api Key: ${cBApiKey} Account Type: ${cBAT}`);
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    const cBData = { username: cBId, password: cBPwd, apiKey: cBApiKey, accountType: cBAT};

    //Snackbar
    const igSnackBar = document.querySelector("#igSnackbar");
    const failedConnection = document.querySelector("#brokerConnectionFailure");


    // Fetch ig account
    const fetchIgAccounts = async () => {
        try{
            const res = await qhr.get("/MVP/fetch_ig_account");
            const accounts = await res;
            // console.log(`Accounts after calling fetch ig accounts - ${accounts}`)
            const accountsData = accounts.data;
            if(!qtlStorage.getItem("IG")){
                qtlStorage.storeItem("IG", accounts.data);
            }
            return accountsData;
        }catch(err){
            console.error(`Error in fetch account - IG ${err}`);
            return err;
        }
        
    }

    if(cBId.length > 4 && cBPwd.length > 4 && cBApiKey.length > 7){

        errorMessage.style.visibility = "hidden";
        const loginBtn = document.querySelector("#connectBrokerLogin");
        loginBtn.textContent = "Loading..."
    
        // change ig credentials  /IGServices/connect_broker
        qhr.post("/IGServices/connect_broker",
        cBData,
        csrftoken)
        .then(resp => {
            console.log("QHR Success Response login data", resp);
            fetchIgAccounts().then((accountsData) => {
                // console.table(accountsData);
                // console.log(`Accounts data -> ${accountsData["pl1"]}`)
                pl1Element.innerHTML += `${accountsData["pl1"]}`;
                pl1_1.innerHTML += `${accountsData["pl1"]}`;
                acc1.innerHTML += `${accountsData["account_1"]}`;
                acc1Blnc.innerHTML += `${accountsData["account_1_balance"]}`;
                acc1Blnc1.innerHTML += `${accountsData["account_1_balance"]}`;
                acc2.innerHTML += `${accountsData["account_2"]}`;
                acc2Blnc.innerHTML += `${accountsData["account_2_balance"]}`;
                igLabel.innerHTML = `Disconnect IG`;
                igConnectedBadge.style.visibility = "visible";
                igConnectedBadge.style.display = "block";
                //showing igdata view
                $emptyBrokerView.style.display = "none";
                $igDataView.style.removeProperty("display");
                //Login Modal Close
                loginBtn.textContent = "Login"
                $("#connectBrokerModal").modal('hide');
                //Clearing the inputs
                document.querySelector("#connectBrokerId").value = "";
                document.querySelector("#connectBrokerPwd").value = "";
                document.querySelector("#connectBrokerApi").value = "";
                igSnackBar.className = "show";
                setTimeout(()=>{
                    igSnackBar.className = igSnackBar.className.replace("show", "");
                },4000);

            }).catch(err => {
                console.error("Fetch ig accounts -> ", err);
                failedConnection.className = "show";
                setTimeout(()=>{
                    failedConnection.className = failedConnection.className.replace("show", "");
                },4000);
            });
            })
            .catch(err => {
                console.error("QHR Failed response login data", err);
                failedConnection.className = "show";
                setTimeout(()=>{
                        failedConnection.className = failedConnection.className.replace("show", "");
                    },4000);
                });
    }else {
        errorMessage.style.visibility = "visible";
    }
    
}

const disconnectIG = () => {
    qtlStorage.removeItem("IG");
    igLabel.innerHTML = `IG`;
    igConnectedBadge.style.visibility = "hidden";
    igConnectedBadge.style.display = "none";
    $igDataView.style.display = "none";
    if(!qtlStorage.getItem('CB') && !qtlStorage.getItem('BN')){
        $emptyBrokerView.style.display = "flex";
    }
}

//Open form for IG
document.querySelector("#connectIG").onclick = () =>{

    if(!qtlStorage.getItem("IG")){
        $('#selectBrokersDropdown').dropdown('dispose');
        $("#connectBrokerModal").modal('show');
    } else {
        disconnectIG();
    }
    
    //for preventing default behaviour
    return false;
}

igDisconnectBadge.onclick = () => {
    disconnectIG();
}