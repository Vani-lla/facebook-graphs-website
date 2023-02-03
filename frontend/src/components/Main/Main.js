import React, { useState, useEffect, Fragment } from 'react';
import './Main.css';


export default function Main() {
    const [loading, setLoading] = useState(true);
    const [data, setData] = useState({});
    const [files, setFiles] = useState([]);
    const [reset, setReset] = useState(false);

    useEffect(() => {
        if (loading) {
            let url = '/api/json/view';
            let http = new XMLHttpRequest();

            http.open("GET", url);
            http.send();
            http.onload = () => {
                let d = http.responseText;
                if (d == "Please log in") {
                    document.location.href = 'api/login';
                }
                console.log(JSON.parse(d).jsons);
                setData(JSON.parse(d).jsons);
                setLoading(false);
            }
        }
    }, [loading])

    useEffect(() => {
        if (!loading) {
            document.getElementById("filepicker").addEventListener("change", (event) => {
                let arr = [];
                for (const file of event.target.files) {
                    if (file.webkitRelativePath.search('.json') !== -1) {
                        let name = file.webkitRelativePath;
                        arr.push(name);
                    }
                };
                // arr.sort((a, b) => {
                //     if (a.name > b.name) {
                //         return 1
                //     } 
                //     return -1
                // })
                arr.sort((a, b) => {
                    if (a.webkitRelativePath > b.webkitRelativePath) {
                        return 1
                    }
                    return -1
                })
                setFiles(arr);
            }, false)
        }
    }, [loading])

    if (loading) {
        return (
            <div className='loader'/>
        )
    } else {
        return (
            <div className='display-jsons'>
                <div className='jsons'>
                    {data.map((json, i) => {
                        return (
                            <a key={i} href={`graph/${json.id}`}>
                                <div>{json.name}</div>
                                <div>{json.size}</div>

                            </a>
                        )
                    })}
                </div>
                <div className='file-upload'>
                    <h2>Add folder with all messages to create graphs!</h2>
                    <div className='inputs'>
                        <input type="file" id="filepicker" name="fileList" webkitdirectory="" multiple=""></input>
                        <button onClick={() => {
                            const files = document.getElementById("filepicker").files;
                            const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
                            let jsons = [];

                            for (const file of files) {
                                if (file.webkitRelativePath.search('.json') !== -1) {
                                    jsons.push(file);
                                }
                            };

                            jsons.sort((a, b) => {
                                if (a.webkitRelativePath > b.webkitRelativePath) {
                                    return 1
                                }
                                return -1
                            });

                            console.log(jsons);

                            let i = 1;
                            let formData = new FormData();
                            let request = new XMLHttpRequest();

                            for (const file of jsons) {
                                i = parseInt(file.name.charAt(file.name.length - 6));
                                if (i === 1) {
                                    console.warn(file.webkitRelativePath);
                                    request = new XMLHttpRequest();
                                    request.open('POST', '/api/json/upload');
                                    request.setRequestHeader("X-CSRFToken", csrftoken);
                                    request.setRequestHeader("enctype", "multipart/form-data");
                                    request.send(formData);
                                    formData = new FormData();

                                    request.onload = () => {
                                        let d = request.responseText;
                                        if (d == "done") {
                                            setLoading(true);
                                        }
                                    }
                                }
                                formData.append('file', file);
                            }
                            request.open('POST', '/api/json/upload');
                            request.setRequestHeader("X-CSRFToken", csrftoken);
                            request.setRequestHeader("enctype", "multipart/form-data");
                            request.send(formData);
                            request.onload = () => {
                                let d = request.responseText;
                                if (d == "done") {
                                    setLoading(true);
                                }
                            };
                        }}>Create graphs</button>
                    </div>
                    <div id='upload-jsons'>
                        {files.map((file, i) => {
                            return (
                                <div key={i}>
                                    {file}
                                </div>
                            )
                        })}
                    </div>
                </div>
            </div>
        )
    }
}
