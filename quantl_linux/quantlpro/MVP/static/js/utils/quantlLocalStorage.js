const qtlStorage = (()=>{
    //public methods
    return {
        storeItem: (key, item) => {
            localStorage.setItem(key, JSON.stringify(item));
        },
        getItem: (key) => {
           const resp = localStorage.getItem(key);
           return JSON.parse(resp);
        },
        clearStorage: () => {
            localStorage.clear();
        },
        removeItem: (key) => {
            localStorage.removeItem(key)
        }
        
    }
})()