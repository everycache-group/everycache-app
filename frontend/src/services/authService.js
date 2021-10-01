import * as api from '../api/api-core';

export async function loginUser(email, password)
{
    let token;

    await api.login(email, password).then(res => { token = res.access_token;});

    return token;
}

export function logoutUser(token)
{
   
}