import React, {useState} from 'react'
import TextField from '@mui/material/TextField'
import Button from '@mui/material/Button'
import * as Style from './style'
import {Redirect} from 'react-router-dom'
import * as user from './../../../services/userService';
import {useStore} from 'react-redux';


function Register() {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

    

    const onRegisterClickHandler = e => {
        e.preventDefault();

        user.create(user)
        
    };


    return (
        <div>
            <Style.RegisterForm>
                <TextField size="small" id="username" onChange={e => setUsername(e.target.value)} type="username" label="Username"/>
                <TextField size="small" id="email" onChange={e => setEmail(e.target.value)} type="email" label="Email"/>
                <TextField size="small" id="password" onChange={e => setPassword(e.target.value)} type="password" label="Password"/>

                <Button  onClick={onRegisterClickHandler} variant="outlined">Register</Button>
            </Style.RegisterForm>
        </div>
    )
}

export default Register
