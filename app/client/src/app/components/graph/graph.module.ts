import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { ChartsModule } from 'ng2-charts';
import { HttpClientModule } from '@angular/common/http';
import { LineChartComponent } from './line/line.component';

@NgModule({
    declarations: [LineChartComponent],
    imports: [BrowserModule, ChartsModule, HttpClientModule],
    providers: [],
    exports: [LineChartComponent],
})
export class GraphModule {}
