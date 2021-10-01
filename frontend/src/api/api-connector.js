import config from './api-config.json'

const {protocol, machine, port} = config.connection;
const apiUrl = `${protocol}://${machine}:${port}`;


export async function sendRequest(action, resource, id = null, params)
{
    const endpoint     = createEndpoint(resource, id);
    const fetchOptions = createfetchOptions(action, params);
    
    const response = await fetch(endpoint, fetchOptions);
    const json     = await response.json();

    console.log(json);

    return json;
}

function createfetchOptions(action, params)
{
    const options = {};

    if(action)
        options.method = action;

    if(params)
        options.body = JSON.stringify(params);

    options.headers = {
        'Content-Type': 'application/json'
    }

    console.log(options);

    return options;
}

function createEndpoint(resource, id = null)
{
    let endpoint = `${apiUrl}/${resource}`;

    if(id) {
        endpoint += `/${id}`
    }
    console.log(endpoint);

    return endpoint;
}



















