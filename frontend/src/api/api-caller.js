import config from './api-config.json'

const {protocol, machine, port} = config.connection;


const apiUrl = `${protocol}://${machine}:${port}/api`;

export async function callAPI(action, resource, id = 0)
{
    const endpoint = `${apiUrl}/${resource}`;

    console.log(endpoint);

    const response = await fetch(endpoint, {
        method: action,
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const json = await response.json();

    return json;
}

