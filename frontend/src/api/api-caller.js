import config from './api-config.json'

const {protocol, machine, port} = config.connection;


const apiUrl = `${protocol}://${machine}:${port}/api/`;

export async function callAPI(action, resource, id = 0)
{
    const endpointURL = apiUrl + resource;

    const response = await fetch(endpointURL, {
        method: action,
        headers: {
            'Content-Type': 'application/json'
        }
    });

    const json = await response.json();

    return json;
}

