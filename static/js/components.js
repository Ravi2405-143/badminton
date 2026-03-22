const Components = {
    TournamentCard(tournament) {
        return `
            <div class="card tournament-card fade-in" onclick="app.showTournament(${tournament.id})">
                <div class="card-icon">
                    <i class="fas ${tournament.sport === 'cricket' ? 'fa-baseball-bat-ball' : 'fa-shuttlecock'}"></i>
                </div>
                <div class="badge">${tournament.sport.toUpperCase()}</div>
                <h3>${tournament.name}</h3>
                <div class="stats" style="margin-top: 1rem; display: flex; gap: 1rem; font-size: 0.8rem; color: var(--text-muted);">
                    <span><i class="fas fa-users"></i> ${tournament.num_participants} Teams</span>
                    <span><i class="fas fa-calendar"></i> ${tournament.format}</span>
                </div>
                <div class="card-footer" style="display: flex; justify-content: flex-end; padding-top: 1.5rem; border-top: 1px solid var(--border); margin-top: 1.5rem;">
                    <button class="btn-danger-outline btn-sm" onclick="event.stopPropagation(); app.deleteTournament(${tournament.id})" title="Delete Tournament"><i class="fas fa-trash"></i></button>
                </div>
            </div>
        `;
    },

    TournamentDashboard(tournament, standings) {
        return `
            <div class="tournament-detail-header fade-in">
                <div class="stats-grid">
                    <div class="card">
                        <h3>Sport</h3>
                        <div class="value">${tournament.sport.toUpperCase()}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">${tournament.is_doubles ? 'Doubles' : 'Singles'} Match</div>
                    </div>
                    <div class="card">
                        <h3>Format</h3>
                        <div class="value">${tournament.format.toUpperCase()}</div>
                        <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.5rem;">Points: ${tournament.points_per_win}W / ${tournament.points_per_draw}D</div>
                    </div>
                    <div class="card">
                        <h3>Participation</h3>
                        <div class="value">${standings.length} / ${tournament.num_participants}</div>
                        <div style="width: 100%; height: 6px; background: var(--border); border-radius: 3px; margin-top: 1rem; overflow: hidden;">
                            <div style="width: ${(standings.length / tournament.num_participants) * 100}%; height: 100%; background: var(--primary);"></div>
                        </div>
                    </div>
                </div>
                <div class="actions-bar" style="display: flex; gap: 1rem; margin-bottom: 3rem;">
                    <button class="btn-secondary" onclick="app.showAddTeam(${tournament.id})"><i class="fas fa-plus"></i> Add Team</button>
                    ${standings.length >= 2 ? `<button class="btn-primary" onclick="app.generateFixtures(${tournament.id})"><i class="fas fa-magic"></i> Generate Fixtures</button>` : ''}
                </div>
            </div>
            
            <div class="dashboard-sections">
                <div class="section">
                    <div class="section-header">
                        <h2>Tournament Fixtures</h2>
                    </div>
                    ${this.FixtureTable(tournament.matches || [])}
                </div>
                <div class="section">
                    <div class="section-header">
                        <h2>Team Standings</h2>
                    </div>
                    ${this.StandingsTable(standings)}
                </div>
            </div>
        `;
    },

    AddTeamForm(tournamentId, isDoubles) {
        return `
            <form id="add-team-form" class="fade-in">
                <input type="hidden" name="tournament_id" value="${tournamentId}">
                <div class="form-group">
                    <label>Team Name</label>
                    <input type="text" name="name" required placeholder="e.g., Lightning Warriors">
                </div>
                <div class="form-group">
                    <label>Player 1 Name (Optional)</label>
                    <input type="text" name="player1" placeholder="Full Name">
                </div>
                ${isDoubles ? `
                <div class="form-group">
                    <label>Player 2 Name (Optional)</label>
                    <input type="text" name="player2" placeholder="Partner Name">
                </div>
                ` : ''}
                <button type="submit" class="btn-primary w-full">Add Team to Tournament</button>
            </form>
        `;
    },

    TournamentList(tournaments) {
        let content = '';
        if (tournaments.length === 0) {
            content = `<div class="empty-state">No tournaments found. Create one to get started!</div>`;
        } else {
            content = `
                <div class="stats-grid">
                    ${tournaments.map(t => this.TournamentCard(t)).join('')}
                </div>
            `;
        }

        return `
            <div class="view-header" style="margin-bottom: 2rem;">
                <button class="btn-primary" onclick="app.showCreateTournament()"><i class="fas fa-plus"></i> Create Tournament</button>
            </div>
            ${content}
        `;
    },

    FixtureTable(fixtures) {
        if (fixtures.length === 0) {
            return `<div class="empty-state">No fixtures generated yet.</div>`;
        }
        return `
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Round</th>
                            <th>Teams</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${fixtures.map(f => `
                            <tr>
                                <td>${f.round_name || 'N/A'}</td>
                                <td>${f.team1 ? f.team1.name : `Team ${f.team1_id}`} vs ${f.team2 ? f.team2.name : `Team ${f.team2_id}`}</td>
                                <td><span class="status-badge ${f.status.toLowerCase()}">${f.status}</span></td>
                                <td>
                                    <button class="btn-sm" onclick="app.showScoring(${f.id})">Score</button>
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },

    StandingsTable(teams) {
        if (teams.length === 0) return '<div class="empty-state">No teams added yet.</div>';
        return `
            <div class="table-container">
                <table>
                    <thead>
                        <tr>
                            <th>Pos</th>
                            <th>Team</th>
                            <th>P</th>
                            <th>W</th>
                            <th>L</th>
                            <th>PG</th>
                            <th>PL</th>
                            <th>Diff (NRR)</th>
                            <th>Pts</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${teams.map((t, i) => `
                            <tr>
                                <td>${i + 1}</td>
                                <td><strong>${t.name}</strong></td>
                                <td>${t.matches_played}</td>
                                <td>${t.wins}</td>
                                <td>${t.losses}</td>
                                <td>${t.points_scored}</td>
                                <td>${t.points_conceded}</td>
                                <td class="${t.nrr >= 0 ? 'text-success' : 'text-danger'}">
                                    ${t.nrr > 0 ? '+' : ''}${Number.isInteger(t.nrr) ? t.nrr : Number(t.nrr.toFixed(3))}
                                </td>
                                <td><strong>${t.points}</strong></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },

    ScoringForm(match, tournament) {
        const isCricket = tournament.sport === 'cricket';
        return `
            <form id="scoring-form" class="fade-in">
                <input type="hidden" name="match_id" value="${match.id}">
                <div class="scoring-grid">
                    <div class="team-score-card">
                        <h4>${match.team1.name}</h4>
                        <div class="form-group">
                            <label>${isCricket ? 'Runs Scored' : 'Sets Won'}</label>
                            <input type="number" name="score1" value="0" min="0" required>
                        </div>
                        ${isCricket ? `
                        <div class="form-group">
                            <label>Wickets Lost</label>
                            <input type="number" name="wickets1" value="0" min="0" max="10">
                        </div>
                        ` : ''}
                    </div>
                    <div class="vs-divider">VS</div>
                    <div class="team-score-card">
                        <h4>${match.team2.name}</h4>
                        <div class="form-group">
                            <label>${isCricket ? 'Runs Scored' : 'Sets Won'}</label>
                            <input type="number" name="score2" value="0" min="0" required>
                        </div>
                        ${isCricket ? `
                        <div class="form-group">
                            <label>Wickets Lost</label>
                            <input type="number" name="wickets2" value="0" min="0" max="10">
                        </div>
                        ` : ''}
                    </div>
                </div>
                <button type="submit" class="btn-primary w-full" style="margin-top: 2rem;">Update Final Score</button>
            </form>
        `;
    },

    RecentResultsView(matches) {
        if (matches.length === 0) return '<div class="empty-state">No matches completed yet.</div>';
        return `
            <div class="table-container fade-in">
                <table>
                    <thead>
                        <tr>
                            <th>Match ID</th>
                            <th>Teams</th>
                            <th>Winner</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${matches.map(m => `
                            <tr>
                                <td>#${m.id}</td>
                                <td>${m.team1.name} vs ${m.team2.name}</td>
                                <td><span class="text-success">${m.winner ? m.winner.name : 'Draw'}</span></td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },

    RankingsView(rankings) {
        if (rankings.length === 0) return '<div class="empty-state">No rankings data available.</div>';
        return `
            <div class="table-container fade-in">
                <table>
                    <thead>
                        <tr>
                            <th>Rank</th>
                            <th>Team</th>
                            <th>Tournament</th>
                            <th>Wins</th>
                            <th>Pts</th>
                            <th>Diff</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${rankings.map((r, i) => `
                            <tr>
                                <td>#${i + 1}</td>
                                <td><strong>${r.team_name}</strong></td>
                                <td>${r.tournament_name}</td>
                                <td>${r.wins}</td>
                                <td>${r.points}</td>
                                <td class="${r.nrr >= 0 ? 'text-success' : 'text-danger'}">${r.nrr > 0 ? '+' : ''}${Number.isInteger(r.nrr) ? r.nrr : Number(r.nrr.toFixed(3))}</td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            </div>
        `;
    },

    CreateTournamentForm() {
        return `
            <form id="create-tournament-form" class="fade-in">
                <div class="form-group">
                    <label>Tournament Name</label>
                    <input type="text" name="name" required placeholder="e.g., Summer League 2024">
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label>Sport</label>
                        <select name="sport">
                            <option value="cricket">Cricket</option>
                            <option value="badminton">Badminton</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Format</label>
                        <select name="format">
                            <option value="league">League (Round Robin)</option>
                            <option value="knockout">Knockout</option>
                        </select>
                    </div>
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label>Total Teams (Capacity)</label>
                        <input type="number" name="num_participants" value="4" min="2">
                    </div>
                    <div class="form-group">
                        <label>Match Type</label>
                        <select name="is_doubles">
                            <option value="false">Singles</option>
                            <option value="true">Doubles</option>
                        </select>
                    </div>
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label>Points per Win</label>
                        <input type="number" name="points_per_win" value="2" min="0">
                    </div>
                    <div class="form-group">
                        <label>Points per Draw</label>
                        <input type="number" name="points_per_draw" value="1" min="0">
                    </div>
                </div>
                <button type="submit" class="btn-primary w-full">Create Tournament</button>
            </form>
        `;
    }
};
