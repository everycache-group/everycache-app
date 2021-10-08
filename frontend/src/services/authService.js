import * as api from '../api/api-core';


export async function loginUser(email, password, callback)
{
    const response =  await api.login(email, password);

    if(response.ok) {
        callback();
    }

}

export async function logoutUser(token)
{
    return await api.logout();  
}