from pyvit.hw.logplayer import LogPlayer


class IDStats:
    def read_frames(self, filename):
        frames = []
        lp = LogPlayer(filename, realtime=False)
        lp.start()

        while True:
            frame = lp.recv()
            if frame is None:
                break
            frames.append(frame)

        return frames

    def read_file(self, filename):
        return self.read_frames(filename)

    def unique_ids(self, frames):
        unique_ids = []
        for frame in frames:
            if frame.arb_id not in unique_ids:
                unique_ids.append(frame.arb_id)
        return unique_ids

    def generate_output(self, frames):
        unique_ids = self.unique_ids(frames)
        id_counts = {}
        id_times = {}

        for frame in frames:
            if frame.arb_id not in unique_ids:
                unique_ids.append(frame.arb_id)

            if frame.arb_id in id_counts:
                id_counts[frame.arb_id] += 1
            else:
                id_counts[frame.arb_id] = 1

            if frame.arb_id in id_times:
                id_times[frame.arb_id].append(frame.timestamp)
            else:
                id_times[frame.arb_id] = [frame.timestamp]

        for arb_id in sorted(unique_ids):
            count = id_counts[arb_id]

            # calculate the average difference of timestamps
            period = 0
            for i in range(1, len(id_times[arb_id])):
                period += id_times[arb_id][i] - id_times[arb_id][i-1]
            period = period / count

            print('0x%3X \t count = %d \t period = %.4f s' %
                  (arb_id, count, period))
