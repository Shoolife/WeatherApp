import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

export default function WeatherChart({ data }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="time" tickFormatter={(t) => new Date(t).getHours() + ":00"} />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="temperature" stroke="#4f46e5" strokeWidth={2} />
      </LineChart>
    </ResponsiveContainer>
  );
}
