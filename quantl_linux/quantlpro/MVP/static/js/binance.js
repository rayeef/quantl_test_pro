(()=>{
    // 
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    
    //Elements Init
    const $binanceLabel = document.querySelector("#binanceLabel");
    const $apiKey = document.querySelector("#binanceKey");
    const $apiSecret = document.querySelector("#binanceSecret");
    const $errorMessage = document.querySelector("#errorMessageBinance");
    const $cancelBtn =  document.querySelector("#binanceCancel");
    const $loginBtn =  document.querySelector("#binanceLogin");

    const $binanceConnectedBadge = document.querySelector("#binanceConnectedBadge");
    const $binanceDisconnectBadge = document.querySelector("#binanceDisconnectBadge");
   
    const $successSnackbar = document.querySelector("#igSnackbar");
    const $failureSnackbar = document.querySelector("#brokerConnectionFailure");

    const $assetsList = document.querySelector("#assetsList");

    const $binanceDataView = document.querySelector('#binanceDataView');
    const $emptyBrokerView = document.querySelector('#emptyBrokerView');
    
    const populateAssetsList = (assetsArray) => {
        $assetsList.innerHTML = ``;
        for(let asset of assetsArray){
            const assetItem = `<div class="row align-items-center justify-content-between border-top p-3 px-md-4 mx-0">
                                <div class="col-sm-auto col-md px-0 pr-sm-3"> ${asset.asset} </div>
                                
                            <div class="col-md text-md-right pt-1 pt-md-0 px-0 pl-md-3">
                                <strong class="d-md-block font-weight-normal">${asset.free} ${asset.asset} </strong>
                            </div>  
                            <div class="col-md pt-md-0 pl-1 pl-md-3" style="display: flex; justify-content: flex-end; align-items: center; " id=${asset.asset}-LG> </div>
                        </div>`;
            
            $assetsList.innerHTML += assetItem;
        }
    }

    const getDate1WeekBefore = () =>{
        const date1WeekBfr = new Date(Date.now() - 7 * 24 * 60 * 60 * 1000);
        const options = { year: 'numeric', month: '2-digit', day: '2-digit' };
        const date = date1WeekBfr.toLocaleDateString("en-US", options).split('/');
        return `${date[2]}-${date[0]}-${date[1]}`;
    }

    const fetchCryptoDataPrevWeek = async (cryptoCode) => {
        const startDate = getDate1WeekBefore();
        const data={cryptoCode: cryptoCode, startDate: startDate};
        try{
            const response = await qhr.post("/MVP/fetch_crypto_data", data, csrftoken);
            const resp = await response?.data;
            // console.log("fetching crypto data previous week",JSON.parse(resp["cryptoValues"]));
            return JSON.parse(resp["cryptoValues"]);
        }catch(err){
            console.trace(`Error in fething crypto error - ${err}`);
            return null;
        } 
    }

    const createLineChart = ($element, data) => {
        let chart = LightweightCharts.createChart($element, {
            width: 80,
            height: 40,
            grid: {
                vertLines: {
                  color: "rgba(197, 203, 206, 0.5)",
                  visible: false,
                },
                horzLines: {
                  color: "rgba(197, 203, 206, 0.5)",
                  visible: false,
                }
              },
        });
        chart.applyOptions({
            priceScale: {
                visible: false,
            },
            timeScale:{
              visible: false,
            },
           
          });
        
        var lineSeries = chart.addLineSeries();
        lineSeries.setData(data);
        chart.timeScale().fitContent();
    }

    const populateCoinLineGraphs = (assetsArray) => {
        console.time("start");
        for(let asset of assetsArray){
            const $element = document.querySelector(`#${asset.asset}-LG`);
            if($element){
                fetchCryptoDataPrevWeek(asset.asset)
                .then((resp)=>{
                    console.log(`Response for ${asset.asset}`, resp);
                    createLineChart($element, resp);
                })
                .catch((err)=>{
                    $element.textContent = "No data"
                })
            }
        }
        console.timeEnd("start");

    }

    // Rest Calls

    const connectBinanceApi = async (data) => {
        try{ 
            const response = await qhr.post("/binance/connect_broker", data, csrftoken);
            const resData = await response.data;
            const accountData = resData["account"];
            return accountData;
        } catch(err){
            console.trace(`Error in connectBinance - ${err}`);
            $failureSnackbar.className = "show";
                setTimeout(()=>{
                        $failureSnackbar.className = $failureSnackbar.className.replace("show", "");
                    },4000);
            
            return null;
        }   
    } 

    const connectSuccess = (data) => {
        let accountData = {...JSON.parse(data), "balances": JSON.parse(data)["balances"].filter(val => val.free > 0)};
        // console.log(console.log("Checking Binance Accounts", accountData)); 
        if(!qtlStorage.getItem("BN") && accountData){
            qtlStorage.storeItem("BN", accountData);
        } 
        populateAssetsList(accountData["balances"]);
        populateCoinLineGraphs(accountData["balances"]);
        $binanceLabel.innerHTML = `Disconnect Binance`;
        $binanceConnectedBadge.style.display = "block";
        $emptyBrokerView.style.display = "none";
        $binanceDataView.style.removeProperty("display");
        //Login Modal Close
        $loginBtn.textContent = "Login";
        $("#connectBinanceModal").modal('hide');
        //Clearing the inputs
        $apiKey.value = "";
        $apiSecret.value = "";

        $successSnackbar.className = "show";
        setTimeout(()=>{
                $successSnackbar.className = $successSnackbar.className.replace("show", "");
            },4000);

    }

    const connectFailure = (err) => {
        $loginBtn.textContent = "Login"
        $apiKey.value = "";
        $apiSecret.value = "";
        console.trace(`Error in connectBinance - ${err}`);
        $failureSnackbar.className = "show";
        setTimeout(()=>{
                $failureSnackbar.className = $failureSnackbar.className.replace("show", "");
            },4000);

    }
    
    //If already logged in
    if(qtlStorage.getItem("BN")){
        const accountsData = qtlStorage.getItem("BN");
        console.log("Data from storage Binance", accountsData);
        populateAssetsList(accountsData["balances"]);
        populateCoinLineGraphs(accountsData["balances"]);
        $binanceLabel.innerHTML = `Disconnect Binance`;
        $binanceConnectedBadge.style.display = "block";
    }else{
        $binanceDataView.style.display = "none";
        if(!qtlStorage.getItem("CB") && !qtlStorage.getItem("IG") && !qtlStorage.getItem("BO")){
            $emptyBrokerView.style.display = "flex";
        }
    }

    // Onclick Listeners

    $loginBtn.onclick = () => {
        if($apiKey.value.length > 0 && $apiSecret.value.length > 0){
            $errorMessage.style.visibility = "hidden";
            $loginBtn.textContent = "Loading...";

            const binanceData = {key: $apiKey.value, secret: $apiSecret.value}; 
            console.log(`Binance Data from frontend -> ${binanceData}`);

            try{
                const connectBinance = async () => {
                    const data = await connectBinanceApi(binanceData);
                    console.log("Data from connectBinanceApi", data);
                    if(data){
                        connectSuccess(data);
                    }else if(!data){
                        connectFailure('Error: Data from connectBinanceApi not handled correctly !')
                    }
                }
                connectBinance();
                
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
        $apiSecret.value = "";
    }


    const disconnectBinance = () => {
        qtlStorage.removeItem("BN");
        $binanceLabel.innerHTML = `Binance`;
        $binanceConnectedBadge.style.display = "none";
        $binanceDataView.style.display = "none";
        if(!qtlStorage.getItem('CB') && !qtlStorage.getItem('IG')){
            $emptyBrokerView.style.display = "flex";
        }
    }

    //Onclick for coinbase tag in dropdown
    document.querySelector("#connectBinance").onclick = () => {
        if(!qtlStorage.getItem("BN")){
            $('#selectBrokersDropdown').dropdown('dispose');
            $("#connectBinanceModal").modal('show');
        } else {
            disconnectBinance();
        }
        //for preventing default behaviour
        return false;
    }

    $binanceDisconnectBadge.onclick = () => {
        disconnectBinance();
    }

})()






