import * as api from '../api/api-core';

export async function loginUser(email, password)
{
 if (!email )
    return;

    await api.login(email, password).then(res => { token = res.access_token;});

    return token;
}

export function logoutUser(token)
{
    return await api.logout();  
}