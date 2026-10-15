import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Fix, Status } from '../../types'

const PANE = 'tracking-list'
// Source of truth. Edit it by hand, from Claude, or with /tracking-list; the pane follows within 2s.
const FILE = '/Users/roywong/.claude/tracking-list.json'

const fixes = atom({ plugin: 'roy-mods', key: 'fixes' } as const, [] as Fix[])

const mark: Record<Status, string> = { todo: '[ ]', wip: '[~]', done: '[x]' }

let lastText = ''

async function load($: any): Promise<Fix[]> {
  try {
    return JSON.parse(await $.fs.read(FILE))
  } catch {
    return []
  }
}

async function save($: any, list: Fix[]) {
  lastText = JSON.stringify(list, null, 1)
  await $.fs.write(FILE, lastText)
  await update($, fixes, () => list)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'tracking-list',
      description: 'Issues needing fixes: pane, set status, add, rm',
    })
    void $.ui.open({ id: PANE, title: 'Tracking list' })
    await update($, fixes, () => [])
    $.clock.every(2000, async () => {
      let text = ''
      try {
        text = await $.fs.read(FILE)
      } catch {
        return
      }
      if (text === lastText) return
      lastText = text
      await update($, fixes, () => {
        try {
          return JSON.parse(text)
        } catch {
          return []
        }
      })
    })

    return next(e)
  })

  // /clear starts a new session with empty $.state and no session.start; force the next poll to reload the file.
  on('classic.SessionStart', async ($, e, next) => {
    if (e.source === 'clear') lastText = ''

    return next(e)
  })

  on('command.run', { command: 'tracking-list' }, async ($, e) => {
    const args = e.args.trim()
    if (!args) {
      await $.ui.open({ id: PANE, title: 'Tracking list' })

      return { text: 'Tracking list pane opened.' }
    }
    const list = await load($)
    // /tracking-list add <HIGH|MED|LOW> <title> | <where>
    const add = args.match(/^add\s+(\S+)\s+(.+?)(?:\s*\|\s*(.*))?$/)
    if (add) {
      const [, sev, title, where = ''] = add
      const n = Math.max(0, ...list.map(f => f.n)) + 1
      await save($, [...list, { n, sev: sev.toUpperCase(), title, where, status: 'todo' as Status }])

      return { text: `Added #${n}.` }
    }
    const [cmd, num, st] = args.split(/\s+/)
    const n = Number(cmd === 'rm' ? num : cmd)
    const status = cmd === 'rm' ? num : st
    if (cmd === 'rm' && Number.isInteger(n)) {
      await save($, list.filter(f => f.n !== n))

      return { text: `#${n} removed` }
    }
    if (!Number.isInteger(n) || !['todo', 'wip', 'done'].includes(status)) {
      return { text: 'Usage: /tracking-list [<n> todo|wip|done | add <sev> <title> | <where> | rm <n>]' }
    }
    await save($, list.map(f => (f.n === n ? { ...f, status: status as Status } : f)))

    return { text: `#${n} -> ${status}` }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const list = await read($, fixes)
    const left = list.filter(f => f.status !== 'done').length

    return (
      <Box flexDirection="column">
        <Text bold>{left} of {list.length} left</Text>
        {list.map(f => (
          <Box flexDirection="column">
            <Text dimColor={f.status === 'done'}>
              {mark[f.status]} {f.n}. {f.sev} {f.title}
            </Text>
            <Text dimColor>      {f.where}</Text>
          </Box>
        ))}
      </Box>
    )
  })
}
