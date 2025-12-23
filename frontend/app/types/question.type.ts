type Question = {
    id: number;
    text: string;
    status: 'Pending' | 'Answered' | 'Escalated';
    createdAt: string;
  };