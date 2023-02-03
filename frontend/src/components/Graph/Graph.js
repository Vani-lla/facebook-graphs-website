import React, { Fragment, useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { Chart as Chartjs } from "chart.js/auto";
import { Line, Doughnut } from "react-chartjs-2";
import './Graph.css';

export default function Graph() {
    let { id } = useParams();
    const [data, setData] = useState({});
    const [loading, setLoading] = useState(true);
    const [number, setNumber] = useState(0);
    const [persons, setPersons] = useState([]);
    const [messages, setMessages] = useState({});
    const [n, setN] = useState(0);
    const [messagesn, setMessagesn] = useState([]);
    const [values, setValues] = useState([]);
    const [pieData, setPieData] = useState([]);

    useEffect(() => {
        let url = `/api/${id}`;
        let http = new XMLHttpRequest();

        http.open("GET", url);
        http.send();
        http.onload = () => {
            let d = http.responseText;
            if (d === "Please log in") return;

            let x = JSON.parse(d);
            let p = Object.keys(x);
            let n = 0;

            let pn = {};
            let u = {};
            let m = {};
            let mmm = {};

            let pieData = [];

            console.log(x);
            console.log(p);

            let a = 0;
            let b = 0;

            for (const date of Object.keys(x[p[0]])) {
                mmm[date] = 0;
                a += 1;
            }

            for (const person of p) {
                pn[person] = 0;
                u[person] = 0;
                m[person] = 0;
                for (const [date, message] of Object.entries(x[person])) {
                    n += message.number;
                    mmm[date] += message.number;
                    pn[person] += message.number;
                    u[person] += message.unsend;
                    m[person] += message.media;
                }
            }
            let xd = [];
            for (const [date, n] of Object.entries(mmm)) {
                if (n > b) {
                    b = n;
                }
                xd.push(n);
            }

            for (const person of p) {
                console.log(person);
                console.log(pn);
                console.log(pn[person]);
                pieData.push(pn[person]);
            }

            setData(x);
            setPersons(p);
            setMessages(mmm);
            setMessagesn(xd);
            setValues(xd);
            setN(20);
            setPieData(pieData);

            setLoading(false);

            // console.log(xd);
            // console.log(Object.keys(mmm));
        }
    }, [])

    useEffect(() => {
        if (!loading) {
            if (n == 0) {
                setValues(messagesn);
            } else {
                let v = [];
                let average_tmp = 0;

                for (let ind = 0; ind < n; ind++) {
                    average_tmp = 0;
                    for (let i = -ind; i <= n; i++) {
                        average_tmp += messagesn[ind + i]
                    }
                    average_tmp /= n;
                    v.push(average_tmp);
                }

                for (let ind = n; ind < messagesn.length; ind++) {
                    average_tmp = 0;
                    for (let i = 0; i <= n; i++) {
                        average_tmp += messagesn[ind - i]
                    }
                    average_tmp /= n;
                    v.push(average_tmp);
                }
                setValues(v);
            }
        }
    }, [n])


    if (loading) {
        return <div className='loader' />
    } else {
        return (
            <div className='graphs-container'>
                <div className='n-slider-container'>
                    <input type="range" min={0} max={40} value={n} id="n-slider" onChange={(event) => {
                        let factor_tmp = event.target.value;
                        setN(factor_tmp);
                    }} />
                </div>
                <div className='graphs'>
                    <div className='line-graph'>
                        <Line
                            data={{
                                "labels": Object.keys(messages),
                                "datasets": [{
                                    "label": 'Wiadomości na dzień',
                                    "data": values,
                                    "fill": true,
                                    "pointRadius": 0,
                                    "tension": .2,
                                }]
                            }}
                        />
                    </div>
                    <div className='chart-container'>
                        <div className='round-graph'>
                            <Doughnut
                                data={{
                                    "labels": persons,
                                    "datasets": [{
                                        "label": "Wysłane wiadomości",
                                        "data": pieData
                                    }]
                                }}
                                options={{
                                    "cutout": 0,
                                }}
                            />
                        </div>
                        <div>

                        </div>
                    </div>
                </div>

            </div>
        )
    }
}
