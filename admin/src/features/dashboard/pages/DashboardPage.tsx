import { Paper, Stack, Typography } from "@mui/material";

const stats = [
  { label: "Residents", value: "—" },
  { label: "Active Bookings", value: "—" },
  { label: "Amenities", value: "—" },
  { label: "Partner Matches", value: "—" },
];

export default function DashboardPage() {
  return (
    <>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Stack direction="row" spacing={2} flexWrap="wrap" useFlexGap>
        {stats.map((stat) => (
          <Paper key={stat.label} sx={{ p: 2, minWidth: 200, flex: "1 1 200px" }}>
            <Typography color="text.secondary">{stat.label}</Typography>
            <Typography variant="h5">{stat.value}</Typography>
          </Paper>
        ))}
      </Stack>
    </>
  );
}
