import CryptoJS from 'crypto-js';

//Encryption__________________________________________________________________________________________
export const GetKey = async() => {
    const response = await fetch("http://127.0.0.1:5000/get-encryption-key", {
        method: 'GET',
    }).catch(err => {
        console.error(err);
    });
    const value = await response.json();
    console.log(`sent value of key `, value)
    const prepared_key = value['key'];
    const iv = value['iv'];
    console.log(`prepared key: ${prepared_key}`);
    return {"prepared_key": prepared_key, "iv": iv}
}

// Symmetric encryption because we utilize a single key for bothe the sender and the receiver
export const Encryption = async (data) => {
    console.log(`[ClientProtocol] [Encryption] data: ${data}`)
    // Define the secret key and payload
    let Key = await GetKey();
    console.log(`KEY: ${Key} `)
    let secretKey = Key["prepared_key"]
    let iv = CryptoJS.enc.Utf8.parse(Key["iv"]);
    // Convert the secret key to a format suitable for encryption
    let derived_key = CryptoJS.enc.Base64.parse(secretKey);

    // Initialize the initialization vector (IV) and encryption mode
    //let iv = CryptoJS.enc.Utf8.parse("1020304050607080");
    let encryptionOptions = {
        iv: iv,
        mode: CryptoJS.mode.CBC
    };

    // Encrypt the payload using AES encryption with the derived key and encryption options
    let encrypted_value = CryptoJS.AES.encrypt(data, derived_key, encryptionOptions).toString();
    console.log(`[ClientProtocol] [Encryption] encrypted data: ${encrypted_value}`)
    return encrypted_value
}

//Client-Server Communication__________________________________________________________________________
//Assume it's already encrypted
const CreateRequestMSG = (data) => {

}

const ReceiveMSGfromServer = async () => {
    const response = await fetch(url, options)
    console.log(response.status)
    if(response.status !== 201  && response.status !== 200){
        const data = await response.json();
        alert(data.message)
    }
}