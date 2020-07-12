export class Temperature {
    id: string;
    location: string;
    timestamp: string;
    value: number;

    constructor(id, location, timestamp, value) {
        this.id = id;
        this.location = location;
        this.timestamp = timestamp;
        this.value = value;
    }
}
