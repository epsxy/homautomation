import { Component, OnInit, ViewChild } from '@angular/core';
import { ChartDataSets, ChartOptions } from 'chart.js';
import { Color, BaseChartDirective, Label } from 'ng2-charts';
import { HttpClient } from '@angular/common/http';

@Component({
    selector: 'app-line-chart',
    templateUrl: './line.component.html',
    styleUrls: ['./line.component.sass'],
})
export class LineChartComponent implements OnInit {
    public lineChartData: ChartDataSets[] = [
        { data: [65, 59, 80, 81, 56, 55, 40], label: 'Series A' },
        { data: [28, 48, 40, 19, 86, 27, 90], label: 'Series B' },
        { data: [180, 480, 770, 90, 1000, 270, 400], label: 'Series C', yAxisID: 'y-axis-1' },
    ];
    public lineChartLabels: Label[] = ['January', 'February', 'March', 'April', 'May', 'June', 'July'];
    public lineChartOptions: ChartOptions & { annotation: any } = {
        responsive: true,
        scales: {
            // We use this empty structure as a placeholder for dynamic theming.
            xAxes: [{}],
            yAxes: [
                {
                    id: 'y-axis-0',
                    position: 'left',
                    ticks: {
                        beginAtZero: true, // minimum value will be 0.
                    },
                },
                {
                    id: 'y-axis-1',
                    position: 'right',
                    gridLines: {
                        color: 'rgba(255,0,0,0.3)',
                    },
                    ticks: {
                        fontColor: 'red',
                    },
                },
            ],
        },
        annotation: {
            annotations: [
                {
                    type: 'line',
                    mode: 'vertical',
                    scaleID: 'x-axis-0',
                    value: 'March',
                    borderColor: 'orange',
                    borderWidth: 2,
                    label: {
                        enabled: true,
                        fontColor: 'orange',
                        content: 'LineAnno',
                    },
                },
            ],
        },
    };
    public lineChartColors: Color[] = [
        {
            // grey
            backgroundColor: 'rgba(148,159,177,0.2)',
            borderColor: 'rgba(148,159,177,1)',
            pointBackgroundColor: 'rgba(148,159,177,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        },
        {
            // dark grey
            backgroundColor: 'rgba(77,83,96,0.2)',
            borderColor: 'rgba(77,83,96,1)',
            pointBackgroundColor: 'rgba(77,83,96,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(77,83,96,1)',
        },
        {
            // red
            backgroundColor: 'rgba(255,0,0,0.3)',
            borderColor: 'red',
            pointBackgroundColor: 'rgba(148,159,177,1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(148,159,177,0.8)',
        },
    ];
    public lineChartLegend = true;
    public lineChartType = 'line';

    @ViewChild(BaseChartDirective, { static: true }) chart: BaseChartDirective;

    constructor(private http: HttpClient) {}

    async ngOnInit(): Promise<void> {
        const res = await this.http.get('http://localhost:9000/api/temperatures').toPromise();
        const temps = [];
        const humidity = [];
        // tslint:disable-next-line:forin
        for (const r in res) {
            temps.push(res[r]);
        }
        console.log(temps);
        this.lineChartData = [];
        this.lineChartLabels = temps.map(t => this.formatDate(t['timestamp']));
        const humidityRes = await this.http.get('http://localhost:9000/api/humidity').toPromise();
        // tslint:disable-next-line:forin
        for (const r in humidityRes) {
            humidity.push(humidityRes[r]);
        }
        this.lineChartData = [
            { data: temps.map(t => t['value']), label: 'Temperature' },
            { data: humidity.map(t => t['value']), label: 'Humidity', yAxisID: 'y-axis-1' },
        ];
        this.chart.update();
    }

    formatDate(timestamp: any): string {
        const date = new Date(timestamp);
        const hours = date.getHours();
        const minutes = date.getMinutes();
        return `${hours}:${minutes}`;
    }

    public randomize(): void {
        for (let i = 0; i < this.lineChartData.length; i++) {
            for (let j = 0; j < this.lineChartData[i].data.length; j++) {
                this.lineChartData[i].data[j] = this.generateNumber(i);
            }
        }
        this.chart.update();
    }

    private generateNumber(i: number): number {
        return Math.floor(Math.random() * (i < 2 ? 100 : 1000) + 1);
    }

    // events
    public chartClicked({ event, active }: { event: MouseEvent; active: {}[] }): void {
        console.log(event, active);
    }

    public chartHovered({ event, active }: { event: MouseEvent; active: {}[] }): void {
        console.log(event, active);
    }

    public hideOne(): void {
        const isHidden = this.chart.isDatasetHidden(1);
        this.chart.hideDataset(1, !isHidden);
    }

    public pushOne(): void {
        this.lineChartData.forEach((x, i) => {
            const num = this.generateNumber(i);
            const data: number[] = x.data as number[];
            data.push(num);
        });
        this.lineChartLabels.push(`Label ${this.lineChartLabels.length}`);
    }

    public changeColor(): void {
        this.lineChartColors[2].borderColor = 'green';
        this.lineChartColors[2].backgroundColor = `rgba(0, 255, 0, 0.3)`;
    }

    public changeLabel(): void {
        this.lineChartLabels[2] = ['1st Line', '2nd Line'];
        // this.chart.update();
    }
}
