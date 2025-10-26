# disc-golf-api
A disc golf REST API.

## API: Event Results

Endpoint: `GET /api/v1/event-results`

Query parameters:
- `disc_event_id` (int): filter by disc event id
- `skip`, `limit` (int): pagination
- `group_by_division` (bool): when true, returns grouped results by division in the shape:

```json
{
	"grouped": [
		{ "division": "MPO", "results": [ /* EventResult objects */ ] },
		{ "division": "FPO", "results": [ /* EventResult objects */ ] }
	]
}
```

- `sort_by_position_raw` (bool): when true, sorts results by numeric `position_raw` with nulls last. Can be combined with `group_by_division`.

Example: `/api/v1/event-results/?disc_event_id=1&group_by_division=true&sort_by_position_raw=true`

