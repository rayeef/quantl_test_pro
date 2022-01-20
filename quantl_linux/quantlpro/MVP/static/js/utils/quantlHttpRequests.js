/** 
*   Custom Http Requests for project - Quantl Http Request
*
*   @version 1.0.0
*   @author  danish: quantl FED
*
**/

class QHR {

    // Get request 
    async get(url) {
        try{
            const response = await fetch(url);
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.log(`Error in QHR - GET - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    // Post request
    /** post -> Expects csrf token */
    async post(url, data, csrfToken) {
        try{
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    'Content-type': 'application/json',
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({data: data}),
                credentials: 'same-origin'
            });
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.log(`Error in QHR - POST - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    // Put request
    async put(url, data) {
        try{
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-type': 'application/json'
                },
                body: JSON.stringify(data),
            });
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.log(`Error in QHR - PUT - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    // DELETE request
    async delete(url, data) {
        try{
            const response = await fetch(url, {
                method: 'DELETE',
                headers: {
                    'Content-type': 'application/json'
                },
                body: JSON.stringify(data),
            });
            const resData = response.json();
            return resData;
        } catch(err) {
            console.log(`Error in QHR - DELETE - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    async postWithQueryString(url, params) {
        try{
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded"
                  },
                body: toQueryString(params),
            });
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.log(`Error in QHR - POST - URL: ${url}`);
            console.log(`${err}`);
        }
    } 

    async getWithAuthBearer(url, authToken) {
        try{
            const response = await fetch(url, {
                headers:{
                    'Authorization': `Bearer ${authToken}`
                }
            });
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.log(`Error in QHR - GET - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    async judge0Post(url, data) {
        try{
            const response = await fetch(url, {
                method: 'POST',
                headers: {
                    'Accept': 'application/json, text/plain, */*',
                    "content-type": "application/json",
		            "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
		            "x-rapidapi-key": "622f460521msh2a814a528caf861p15db9ejsn704dc32d7e35"
                },
                body: JSON.stringify(data),
                credentials: 'same-origin'
            });
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.trace(`Error in QHR - POST - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    async judge0Get(url) {
        try{
            const response = await fetch(url, {
                headers:{
                    "x-rapidapi-host": "judge0-ce.p.rapidapi.com",
		            "x-rapidapi-key": "622f460521msh2a814a528caf861p15db9ejsn704dc32d7e35"
                }
            });
            const resData = await response.json();
            return resData;
        } catch(err) {
            console.trace(`Error in QHR Judge0 - GET - URL: ${url}`);
            console.log(`${err}`);
        }
    }

    
}

const qhr = new QHR;