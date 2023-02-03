import React, { useState, useEffect } from 'react';
import './Status.css';

export default function Status() {
    const [login, setLogin] = useState('Nikt');

    useEffect(() => {
        let url = '/api/who';
        let http = new XMLHttpRequest();

        http.open("GET", url);
        http.send();
        http.onload = () => {
            let d = http.responseText;
            setLogin(d);
        }
    }, [])

    return (
        <div className='status'>
            <div className='username'>{login}</div>
            <a className='logout' href='/api/logout'>logout</a>
        </div>
    )

}
