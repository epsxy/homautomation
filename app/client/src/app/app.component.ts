import { Component, OnInit } from '@angular/core';
import { ChartType } from 'chart.js';
import { HttpClient } from '@angular/common/http';
import { Temperature } from './model/temperature.model';

@Component({
    selector: 'app-root',
    templateUrl: './app.component.html',
    styleUrls: ['./app.component.sass'],
})
export class AppComponent implements OnInit {
    constructor(private http: HttpClient) {}

    public canGraphBeDisplayed = false;
    public barChartOptions = {
        scaleShowVerticalLines: false,
        responsive: true,
        scales: {
            yAxes: [
                {
                    display: true,
                    ticks: {
                        beginAtZero: true, // minimum value will be 0.
                    },
                },
            ],
        },
    };
    public barChartLabels = [];
    public barChartType: ChartType = 'bar';
    public barChartLegend = true;
    public barChartData = [];

    async ngOnInit(): Promise<void> {
        const res = await this.http.get('http://localhost:9000/api/temperatures').toPromise();
        const temps = [];
        // tslint:disable-next-line:forin
        for (const r in res) {
            temps.push(res[r]);
        }
        console.log(temps);
        this.barChartLabels = temps.map(t => this.formatDate(t['timestamp']));
        this.barChartData.push({ data: temps.map(t => t['value']), label: 'Sandbox' });
        this.canGraphBeDisplayed = true;
    }

    formatDate(timestamp: any): string {
        const date = new Date(timestamp);
        const hours = date.getHours();
        const minutes = date.getMinutes();
        return `${hours}:${minutes}`;
    }
}
