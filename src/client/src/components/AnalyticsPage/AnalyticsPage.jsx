import React, { useContext, useEffect, useState } from 'react';
import Plot from 'react-plotly.js';
import './index.css';
import Loader from '../Loader/Loader';

const AnalyticsPage = () => {
    const [loanStatusHist, setLoanStatusHist] = useState(null);
    const [featureImportanceBar, setFeatureImportanceBar] = useState(null);

    useEffect(() => {
        const fetchPlot = async () => {
            try {
                let loanStatusHistResponse = await fetch('https://bc-loan-application-server.onrender.com/analytics/loan_status_hist', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                let data = await loanStatusHistResponse.json();
                console.log(data)
                setLoanStatusHist(data);

                let featureImportanceBarResponse = await fetch('https://bc-loan-application-server.onrender.com/analytics/feature_importance_bar', {
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                });
                data = await featureImportanceBarResponse.json();
                console.log(data)
                setFeatureImportanceBar(data);

                // response = await fetch('http://localhost:5000/analytics/loan_status_hist', {
                //     method: 'GET',
                //     headers: {
                //         'Content-Type': 'application/json',
                //     },
                // });
                // data = await response.json();
                // setLoanStatusHist(data);

                // response = await fetch('http://localhost:5000/analytics/loan_status_hist', {
                //     method: 'GET',
                //     headers: {
                //         'Content-Type': 'application/json',
                //     },
                // });
                // data = await response.json();
                // setLoanStatusHist(data);


            } catch (error) {
                console.error('Error fetching plot data:', error);
            }
        };

        fetchPlot();
    }, []);

    return (
        <div>
            <div className='analytics-graphing-container'>
                {loanStatusHist && featureImportanceBar ? <>
                    <Plot data={loanStatusHist.data} layout={loanStatusHist.layout} />
                    <Plot data={featureImportanceBar.data} layout={featureImportanceBar.layout} />
                </> :
                    <Loader />
                }
            </div>
        </div>
    );
};

export default AnalyticsPage;