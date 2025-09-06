import { useEffect, useState } from 'react';
import { getBrief } from '../lib/api';
import { BriefResult, Claim } from '../lib/types';
import { save } from '../lib/storage';
import { useNavigate } from 'react-router-dom';

export default function MorningBrief() {
  const [userId, setUserId] = useState('U1');
  const [date, setDate] = useState(() => new Date().toISOString().slice(0, 10));
  const [brief, setBrief] = useState<BriefResult | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    getBrief(userId, date).then(setBrief).catch(() => {});
  }, [userId, date]);

  function openClaim(c: Claim) {
    save(c);
    nav('/');
  }

  return (
    <div className="p-4">
      <h2>Morning Brief</h2>
      <div className="flex gap-2 mb-4">
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} />
        <select value={userId} onChange={(e) => setUserId(e.target.value)}>
          <option value="U1">U1</option>
          <option value="U2">U2</option>
        </select>
      </div>
      {brief && (
        <>
          <h3>Highlights</h3>
          <ul>
            {brief.highlights.map((h, i) => (
              <li key={i}>{h}</li>
            ))}
          </ul>
          <h3>Queue</h3>
          <table>
            <thead>
              <tr>
                <th>Score</th>
                <th>Claim</th>
                <th>Why</th>
                <th>ETA</th>
                <th>Δ$</th>
                <th>Deadline</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {brief.queue.map((q, i) => (
                <tr key={i} style={{ fontWeight: i === 0 ? 'bold' : undefined }}>
                  <td>{q.score}</td>
                  <td>{JSON.stringify(q.claim).slice(0, 20)}...</td>
                  <td>{q.why}</td>
                  <td>{q.eta}</td>
                  <td>{q.delta}</td>
                  <td>{q.deadline}</td>
                  <td>
                    <button onClick={() => openClaim(q.claim)}>Open in Workbench</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </>
      )}
    </div>
  );
}
