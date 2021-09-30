import url from './url-resolver';
import config from './api-config.json'

const resources = config.resources;
const url = url();

export async  function getAllUsers()
{
    const response = await fetch(`${url}`)
    const users = await response.json();

    return users;
}


