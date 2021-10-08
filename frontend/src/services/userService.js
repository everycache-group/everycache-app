import * as api from './../api/api-core'

const userResource = api.resources.user;

//tested
export async function create(username, email, password)
{
    return await api.create(userResource, { username, email, password });
}

//TODO check it
export async function get(userId, email, password)
{
    return await api.get(userResource, userId);
}

//TODO check it
export async function getAll(token)
{
    return await api.get(userResource);
}

//TODO check it
export async function deleteUser(userId, token)
{
    return await api.remove(userResource, userId);
}
