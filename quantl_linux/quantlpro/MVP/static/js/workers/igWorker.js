const secretCache = {};
const fetchAccountsUrl = `/MVP/fetch_ig_account`;
 

onmessage = async (userId) => {
    if(!secretCache.userId){
        //fetching user secret token
        console.log(`Fetching User secret token ${userId}`);
    }
    let resData="";
    try{
        const response = await fetch(fetchAccountsUrl);
        resData = await response.json();
    } catch(err) {
        console.log(`Error in Igworker - GET - URL: ${fetchAccountsUrl}`);
        console.log(`${err}`);
    }
    console.log(`Accounts after calling fetch ig accounts - ${resData}`);
    console.table(resData);
    postMessage(resData);
}