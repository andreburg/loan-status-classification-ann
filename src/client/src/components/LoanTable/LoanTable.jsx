import React, { useContext, useEffect, useState } from 'react';
import {
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    TablePagination,
} from '@mui/material';
import './index.css'
import { loanApplicationsContext } from '../../lib/Context';

const LoanTable = () => {
    const [filteredApplications, setFilteredApplications] = useState([]);
    const [loanApplications, setLoanApplications] = useContext(loanApplicationsContext);
    const [rowsPerPage, setRowsPerPage] = useState(10);
    const [page, setPage] = useState(0);
    const attributes = ['loan_id', 'gender', 'married', 'dependents', 'education', 'self_employed', 'applicant_income', 'coapplicant_income', 'loan_amount', 'loan_amount_term', 'credit_history', 'property_area', 'loan_status']

    const handleChangePage = (event, newPage) => {
        setPage(newPage);
    };

    const handleChangeRowsPerPage = (event) => {
        setRowsPerPage(parseInt(event.target.value, 10));
        setPage(0);
    };

    useEffect(() => {
        let sortedApplications = loanApplications.sort((a, b) => {
            const numericA = parseInt(a.loan_id.substring(2));
            const numericB = parseInt(b.loan_id.substring(2));
            return numericB - numericA;
        });

        setFilteredApplications(loanApplications.filter((_, i) => (i < rowsPerPage * page + rowsPerPage && i >= rowsPerPage * page)))
    }, [loanApplications, page, rowsPerPage])

    useEffect(() => {
        fetch('http://localhost:5000/loans', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(async res => {
            let loans = await res.json()
            setLoanApplications(loans)
        })
    }, [])

    return (
        <>
            <Table>
                <TableHead>
                    <TableRow>
                        {
                            attributes.map((a, i) =>
                                <TableCell key={i} sx={{ fontWeight: "bold" }} style={{ fontSize: '0.8rem' }}>{a.split('_').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(" ")}</TableCell>
                            )
                        }
                    </TableRow>
                </TableHead>
                <TableBody>
                    {filteredApplications.map((loan, i) => (
                        <TableRow key={i}>
                            {
                                attributes.map((k, i) => <>
                                    {loan[k] || loan[k] == 0 ?
                                        <TableCell key={i} style={{ fontSize: '0.75rem', minWidth: 75, color: k == 'loan_status' ? loan[k] === 'Approved' ? 'green' : 'red' : 'black' }} >{loan[k]}</TableCell>
                                        :
                                        <TableCell key={i} style={{ fontSize: '0.75rem', minWidth: 75 }}>NaN</TableCell>
                                    }
                                </>)
                            }
                        </TableRow>
                    ))}
                </TableBody>
            </Table>

            <TablePagination
                rowsPerPageOptions={[10, 15, 20]}
                component="div"
                count={loanApplications.length}
                rowsPerPage={rowsPerPage}
                page={page}
                onPageChange={handleChangePage}
                onRowsPerPageChange={handleChangeRowsPerPage}
            />
        </>

    );
};

export default LoanTable;
