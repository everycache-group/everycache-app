import * as api from './../api/api-core'
import { useSelector } from 'react-redux';

const userResource = api.resources.user;

export async function create(username, login, password)
{
    return await api.create(userResource, { username, login, password });
}


